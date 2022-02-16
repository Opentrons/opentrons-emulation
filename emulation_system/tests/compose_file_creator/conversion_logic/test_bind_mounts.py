"""Tests related to bind mounts."""
from typing import (
    Any,
    Dict,
    List,
)

import py
import pytest
from pytest_lazyfixture import lazy_fixture

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.compose_file_model import Service
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    SourceType,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)
from tests.compose_file_creator.conversion_logic.conftest import partial_string_in_mount


@pytest.fixture
def ot3_firmware_dir(tmpdir: py.path.local) -> str:
    """Get path to temporary opentrons-modules directory.

    Note that this variable is scoped to the test. So if you call the fixture from
    different places in the test the variable will be the same.
    """
    return str(tmpdir.mkdir("ot3-firmware"))


@pytest.fixture
def ot3_local_source_local_robot(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    ot3_default["source-type"] = SourceType.LOCAL
    ot3_default["source-location"] = ot3_firmware_dir
    ot3_default["robot-server-source-type"] = SourceType.LOCAL
    ot3_default["robot-server-source-location"] = opentrons_dir
    return convert_from_obj({"robot": ot3_default}, testing_global_em_config)


@pytest.fixture
def ot3_local_source_remote_robot(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    ot3_default["source-type"] = SourceType.LOCAL
    ot3_default["source-location"] = ot3_firmware_dir
    ot3_default["robot-server-source-type"] = SourceType.REMOTE
    ot3_default["robot-server-source-location"] = "latest"
    return convert_from_obj({"robot": ot3_default}, testing_global_em_config)


@pytest.fixture
def ot3_remote_source_local_robot(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    ot3_default["source-type"] = SourceType.REMOTE
    ot3_default["source-location"] = "latest"
    ot3_default["robot-server-source-type"] = SourceType.LOCAL
    ot3_default["robot-server-source-location"] = opentrons_dir
    return convert_from_obj({"robot": ot3_default}, testing_global_em_config)


@pytest.fixture
def ot3_remote_source_remote_robot(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    ot3_default["source-type"] = SourceType.REMOTE
    ot3_default["source-location"] = "latest"
    ot3_default["robot-server-source-type"] = SourceType.REMOTE
    ot3_default["robot-server-source-location"] = "latest"
    return convert_from_obj({"robot": ot3_default}, testing_global_em_config)


@pytest.mark.parametrize("service_name", [HEATER_SHAKER_MODULE_ID])
def test_service_without_bind_mounts(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Verify services without volumes don't have volumes."""
    assert robot_with_mount_and_modules_services[service_name].volumes is None


@pytest.mark.parametrize(
    "service_name,expected_mounts",
    [
        [
            OT2_ID,
            ["opentrons:/opentrons", "entrypoint.sh:/entrypoint.sh"],
        ],
        # Thermocycler should be bound to /opentrons-modules because it is using
        # hardware level emulation
        [
            THERMOCYCLER_MODULE_ID,
            ["opentrons-modules:/opentrons-modules", "entrypoint.sh:/entrypoint.sh"],
        ],
        [MAGNETIC_MODULE_ID, ["opentrons:/opentrons", "entrypoint.sh:/entrypoint.sh"]],
        [
            TEMPERATURE_MODULE_ID,
            ["opentrons:/opentrons", "entrypoint.sh:/entrypoint.sh"],
        ],
    ],
)
def test_service_with_bind_mounts(
    service_name: str,
    expected_mounts: List[str],
    robot_with_mount_and_modules_services: Dict[str, Service],
) -> None:
    """Verify services without volumes don't have volumes."""
    volumes = robot_with_mount_and_modules_services[service_name].volumes
    assert volumes is not None
    for mount in expected_mounts:
        assert any([mount in volume for volume in volumes])


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_local_source_local_robot"),
        lazy_fixture("ot3_remote_source_local_robot"),
    ],
)
def test_robot_server_with_local_mounts(config: RuntimeComposeFileModel) -> None:
    """Confirm local mounts on robot server are working correctly.

    Test that when a local robot-sever-source-type is specified that the source
    mounted in is the source specified in robot-server-source-location. Also make
    sure that entrypoint.sh is bound in.
    """
    robot_server = config.robot_server
    assert robot_server is not None
    assert partial_string_in_mount("opentrons:/opentrons", robot_server)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server)
    assert not partial_string_in_mount("ot3-firmware:/ot3-firmware", robot_server)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_local_source_remote_robot"),
        lazy_fixture("ot3_remote_source_remote_robot"),
    ],
)
def test_robot_server_with_remote_mounts(config: RuntimeComposeFileModel) -> None:
    """Confirm nothing is mounted when robot server is set to remote."""
    robot_server = config.robot_server
    assert robot_server is not None
    assert robot_server.volumes is None


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_local_source_remote_robot"),
        lazy_fixture("ot3_local_source_local_robot"),
    ],
)
def test_ot3_firmware_services_with_local_mounts(
    config: RuntimeComposeFileModel,
) -> None:
    """Confirm ot3 firmware and entrypoint.sh are mounted to OT3 services."""
    assert config.ot3_emulators is not None
    for emulator in config.ot3_emulators:
        assert not partial_string_in_mount("opentrons:/opentrons", emulator)
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", emulator)
        assert partial_string_in_mount("ot3-firmware:/ot3-firmware", emulator)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_remote_source_remote_robot"),
        lazy_fixture("ot3_remote_source_local_robot"),
    ],
)
def test_ot3_firmware_services_with_remote_mounts(
    config: RuntimeComposeFileModel,
) -> None:
    """Confirm nothing is mounted to OT3 Emulators when source-type is set to remote."""
    assert config.ot3_emulators is not None
    for emulator in config.ot3_emulators:
        assert emulator.volumes is None
