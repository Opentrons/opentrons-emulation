"""Tests related to bind mounts."""
from typing import Any, Callable, Dict, Optional

import py
import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    SourceType,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from tests.compose_file_creator.conversion_logic.conftest import partial_string_in_mount


@pytest.fixture
def set_source_type_params(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    def _set_source_type_params(
        robot_dict: Dict[str, Any],
        source_type: SourceType,
        source_location: str,
        robot_server_source_type: SourceType,
        robot_server_source_location: str,
        can_server_source_type: Optional[SourceType],
        can_server_source_location: Optional[str],
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
def ot3_remote_everything(
    ot3_default: Dict[str, Any], set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.REMOTE,
        can_server_source_location="latest",
    )


@pytest.fixture
def ot3_local_robot(
    ot3_default: Dict[str, Any], opentrons_dir: str, set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type="remote",
        can_server_source_location="latest",
    )


@pytest.fixture
def ot3_local_source(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    set_source_type_params: Callable,
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.LOCAL,
        source_location=ot3_firmware_dir,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.REMOTE,
        can_server_source_location="latest",
    )


@pytest.fixture
def ot3_local_can(
    ot3_default: Dict[str, Any], opentrons_dir: str, set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.LOCAL,
        can_server_source_location=opentrons_dir,
    )


@pytest.fixture
def ot2_local_source(
    ot2_default: Dict[str, Any], opentrons_dir: str, set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.LOCAL,
        source_location=opentrons_dir,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=None,
        can_server_source_location=None,
    )


@pytest.fixture
def ot2_local_robot(
    ot2_default: Dict[str, Any], opentrons_dir: str, set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type=None,
        can_server_source_location=None,
    )


def test_ot3_remote_everything(ot3_remote_everything: RuntimeComposeFileModel) -> None:
    """Confirm nothing is mounted when robot server is set to remote."""
    robot_server = ot3_remote_everything.robot_server
    can_server = ot3_remote_everything.can_server
    emulators = ot3_remote_everything.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None
    assert can_server.volumes is None
    for emulator in ot3_remote_everything.ot3_emulators:
        assert emulator.volumes is None


def test_ot3_local_source(ot3_local_source: RuntimeComposeFileModel) -> None:
    """Confirm nothing is mounted when robot server is set to remote."""
    robot_server = ot3_local_source.robot_server
    can_server = ot3_local_source.can_server
    emulators = ot3_local_source.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None
    assert can_server.volumes is None
    for emulator in ot3_local_source.ot3_emulators:
        assert len(emulator.volumes) == 2
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", emulator.volumes)
        assert partial_string_in_mount("ot3-firmware:/ot3-firmware", emulator.volumes)


def test_ot3_local_can_server(ot3_local_can: RuntimeComposeFileModel) -> None:
    """Confirm nothing is mounted when robot server is set to remote."""
    robot_server = ot3_local_can.robot_server
    can_server = ot3_local_can.can_server
    emulators = ot3_local_can.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None
    assert partial_string_in_mount("opentrons:/opentrons", can_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", can_server.volumes)
    assert len(can_server.volumes) == 2
    for emulator in ot3_local_can.ot3_emulators:
        assert emulator.volumes is None


def test_ot3_local_robot_server(ot3_local_robot: RuntimeComposeFileModel) -> None:
    """Confirm nothing is mounted when robot server is set to remote."""
    robot_server = ot3_local_robot.robot_server
    can_server = ot3_local_robot.can_server
    emulators = ot3_local_robot.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert partial_string_in_mount("opentrons:/opentrons", robot_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server.volumes)
    assert len(robot_server.volumes) == 2
    assert can_server.volumes is None
    for emulator in ot3_local_robot.ot3_emulators:
        assert emulator.volumes is None


def test_ot2_local_robot_server(ot2_local_robot: RuntimeComposeFileModel) -> None:
    """Confirm nothing is mounted when robot server is set to remote."""
    robot_server = ot2_local_robot.robot_server
    smoothie = ot2_local_robot.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert partial_string_in_mount("opentrons:/opentrons", robot_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server.volumes)
    assert len(robot_server.volumes) == 2
    assert smoothie.volumes is None


def test_ot2_local_source(ot2_local_source: RuntimeComposeFileModel) -> None:
    """Confirm nothing is mounted when robot server is set to remote."""
    robot_server = ot2_local_source.robot_server
    smoothie = ot2_local_source.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert partial_string_in_mount("opentrons:/opentrons", smoothie.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", smoothie.volumes)
    assert len(smoothie.volumes) == 2
    assert robot_server.volumes is None
