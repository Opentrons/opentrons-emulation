"""Tests related to bind mounts."""
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
)

import py
import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

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
def set_source_type_params(
    testing_global_em_config: OpentronsEmulationConfiguration
) -> Callable:
    def _set_source_type_params(
        robot_dict: Dict[str, Any],
        source_type: SourceType,
        source_location: str,
        robot_server_source_type: SourceType,
        robot_server_source_location: str,
        can_server_source_type: Optional[SourceType],
        can_server_source_location: Optional[str]
    ) -> RuntimeComposeFileModel:
        robot_dict["source-type"] = source_type
        robot_dict["source-location"] = source_location
        robot_dict["robot-server-source-type"] = robot_server_source_type
        robot_dict["robot-server-source-location"] = robot_server_source_location

        if (
                can_server_source_type is not None
                and can_server_source_location is not None
        ):
            robot_dict["can-server-source-type"] = can_server_source_type
            robot_dict["can-server-source-location"] = can_server_source_location

        return convert_from_obj({"robot": robot_dict}, testing_global_em_config)

    return _set_source_type_params


@pytest.fixture
def ot3_firmware_dir(tmpdir: py.path.local) -> str:
    """Get path to temporary opentrons-modules directory.

    Note that this variable is scoped to the test. So if you call the fixture from
    different places in the test the variable will be the same.
    """
    return str(tmpdir.mkdir("ot3-firmware"))


@pytest.fixture
def ot3_local_source_local_robot_remote_can(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.LOCAL,
        source_location=ot3_firmware_dir,
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type="remote",
        can_server_source_location="latest"
    )


@pytest.fixture
def ot3_local_source_remote_robot_remote_can(
    ot3_default: Dict[str, Any],
    ot3_firmware_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.LOCAL,
        source_location=ot3_firmware_dir,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type="remote",
        can_server_source_location="latest"
    )


@pytest.fixture
def ot3_remote_source_local_robot_remote_can(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type="remote",
        can_server_source_location="latest"
    )


@pytest.fixture
def ot3_remote_source_remote_robot_remote_can(
    ot3_default: Dict[str, Any],
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type="remote",
        can_server_source_location="latest"
    )


@pytest.fixture
def ot3_local_source_local_robot_local_can(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.LOCAL,
        source_location=ot3_firmware_dir,
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type=SourceType.LOCAL,
        can_server_source_location=opentrons_dir
    )


@pytest.fixture
def ot3_local_source_remote_robot_local_can(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.LOCAL,
        source_location=ot3_firmware_dir,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.LOCAL,
        can_server_source_location=opentrons_dir
    )


@pytest.fixture
def ot3_remote_source_local_robot_local_can(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type=SourceType.LOCAL,
        can_server_source_location=opentrons_dir
    )


@pytest.fixture
def ot3_remote_source_remote_robot_local_can(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.LOCAL,
        can_server_source_location=opentrons_dir
    )


@pytest.fixture
def ot2_local_source_local_robot(
    ot2_default: Dict[str, Any],
    opentrons_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.LOCAL,
        source_location=opentrons_dir,
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type=None,
        can_server_source_location=None
    )


@pytest.fixture
def ot2_local_source_remote_robot(
    ot2_default: Dict[str, Any],
    opentrons_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.LOCAL,
        source_location=opentrons_dir,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=None,
        can_server_source_location=None
    )


@pytest.fixture
def ot2_remote_source_local_robot(
    ot2_default: Dict[str, Any],
    opentrons_dir: str,
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type=None,
        can_server_source_location=None
    )


@pytest.fixture
def ot2_remote_source_remote_robot(
    ot2_default: Dict[str, Any],
    set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=None,
        can_server_source_location=None
    )


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
        lazy_fixture("ot2_local_source_local_robot"),
        lazy_fixture("ot2_remote_source_local_robot"),
        lazy_fixture("ot3_local_source_local_robot_remote_can"),
        lazy_fixture("ot3_remote_source_local_robot_remote_can"),
        lazy_fixture("ot3_local_source_local_robot_local_can"),
        lazy_fixture("ot3_remote_source_local_robot_local_can"),
    ],
)
def test_robot_server_with_local_mounts(config: RuntimeComposeFileModel) -> None:
    """Confirm local mounts on robot server are working correctly.

    Test that when a local robot-sever-source-type is specified that the source
    mounted in is the source specified in robot-server-source-location. Also make
    sure that entrypoint.sh is bound in.
    """
    print(config)
    robot_server = config.robot_server
    assert robot_server is not None
    assert partial_string_in_mount("opentrons:/opentrons", robot_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server.volumes)
    assert not partial_string_in_mount(
        "ot3-firmware:/ot3-firmware",
        robot_server.volumes
    )


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot2_local_source_remote_robot"),
        lazy_fixture("ot2_remote_source_remote_robot"),
        lazy_fixture("ot3_local_source_remote_robot_remote_can"),
        lazy_fixture("ot3_remote_source_remote_robot_remote_can"),
        lazy_fixture("ot3_local_source_remote_robot_local_can"),
        lazy_fixture("ot3_remote_source_remote_robot_local_can"),
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
        lazy_fixture("ot3_local_source_remote_robot_remote_can"),
        lazy_fixture("ot3_local_source_local_robot_remote_can"),
        lazy_fixture("ot3_local_source_remote_robot_local_can"),
        lazy_fixture("ot3_local_source_local_robot_local_can"),
    ],
)
def test_ot3_firmware_services_with_local_mounts(
    config: RuntimeComposeFileModel,
) -> None:
    """Confirm ot3 firmware and entrypoint.sh are mounted to OT3 services."""
    assert config.ot3_emulators is not None
    for emulator in config.ot3_emulators:
        assert len(emulator.volumes) == 2
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", emulator.volumes)
        assert partial_string_in_mount("ot3-firmware:/ot3-firmware", emulator.volumes)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_remote_source_remote_robot_remote_can"),
        lazy_fixture("ot3_remote_source_local_robot_remote_can"),
        lazy_fixture("ot3_remote_source_remote_robot_local_can"),
        lazy_fixture("ot3_remote_source_local_robot_local_can"),
    ],
)
def test_ot3_firmware_services_with_remote_mounts(
    config: RuntimeComposeFileModel,
) -> None:
    """Confirm nothing is mounted to OT3 Emulators when source-type is set to remote."""
    assert config.ot3_emulators is not None
    for emulator in config.ot3_emulators:
        assert emulator.volumes is None


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_local_source_local_robot_remote_can"),
        lazy_fixture("ot3_local_source_remote_robot_remote_can"),
        lazy_fixture("ot3_remote_source_local_robot_remote_can"),
        lazy_fixture("ot3_remote_source_remote_robot_remote_can"),
    ],
)
def test_can_server_with_remote_mounts(config: RuntimeComposeFileModel) -> None:
    """Confirm nothing is mounted to CAN server when can-server-source-type is remote."""  # noqa: E501
    can_server = config.can_server
    assert can_server is not None
    assert can_server.volumes is None


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_local_source_local_robot_local_can"),
        lazy_fixture("ot3_local_source_remote_robot_local_can"),
        lazy_fixture("ot3_remote_source_local_robot_local_can"),
        lazy_fixture("ot3_remote_source_remote_robot_local_can"),
    ],
)
def test_can_server_with_local_mounts(config: RuntimeComposeFileModel) -> None:
    """Confirm monorepo mounted to CAN server when can-server-source-type is local."""  # noqa: E501
    can_server = config.can_server
    assert can_server is not None
    assert partial_string_in_mount("opentrons:/opentrons", can_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", can_server.volumes)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot2_local_source_remote_robot"),
        lazy_fixture("ot2_local_source_local_robot"),
    ],
)
def test_ot2_firmware_services_with_local_mounts(
    config: RuntimeComposeFileModel,
) -> None:
    """Confirm monorepo and entrypoint.sh are mounted to smoothie emulator."""
    assert config.smoothie_emulator is not None
    volumes = config.smoothie_emulator.volumes
    assert volumes is not None
    assert len(volumes) == 2
    assert partial_string_in_mount("opentrons:/opentrons", volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", volumes)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot2_remote_source_local_robot"),
        lazy_fixture("ot2_remote_source_remote_robot"),
    ],
)
def test_ot2_firmware_services_with_remote_mounts(
    config: RuntimeComposeFileModel,
) -> None:
    """Confirm nothing is mounted to smoothie emulator."""
    assert config.smoothie_emulator is not None
    assert config.smoothie_emulator.volumes is None
