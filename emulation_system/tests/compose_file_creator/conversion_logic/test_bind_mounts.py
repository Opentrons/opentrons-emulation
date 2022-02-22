"""Tests related to bind mounts."""
from typing import Any, Callable, Dict, Optional, cast

import py
import pytest

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Service,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    OpentronsRepository,
    RepoToBuildArgMapping,
    SourceType,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from tests.compose_file_creator.conversion_logic.conftest import partial_string_in_mount


def get_source_code_build_args(service: Service) -> Dict[str, str]:
    """Get build args for service."""
    build = service.build
    assert build is not None
    assert isinstance(build, BuildItem)
    assert build.args is not None
    return cast(Dict[str, str], build.args.__root__)


def build_args_are_none(service: Service) -> bool:
    """Whether or not build args are None. With annoying typing stuff."""
    build = service.build
    assert build is not None
    assert isinstance(build, BuildItem)
    return build.args is None


@pytest.fixture
def set_source_type_params(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    """Create a runnable fixture that builds a RuntimeComposeFileModel."""

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
def ot2_remote_everything(
    ot2_default: Dict[str, Any], set_source_type_params: Callable
) -> RuntimeComposeFileModel:
    """Get OT3 configured for local source and local robot source."""
    return set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=None,
        can_server_source_location=None,
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


@pytest.fixture
def opentrons_head(testing_global_em_config: OpentronsEmulationConfiguration) -> str:
    """Return head of opentrons repo from test config file."""
    return testing_global_em_config.get_repo_head(OpentronsRepository.OPENTRONS)


@pytest.fixture
def ot3_firmware_head(testing_global_em_config: OpentronsEmulationConfiguration) -> str:
    """Return head of ot3-firmware repo from test config file."""
    return testing_global_em_config.get_repo_head(OpentronsRepository.OT3_FIRMWARE)


def test_ot3_remote_everything_mounts(
    ot3_remote_everything: RuntimeComposeFileModel,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when all source-types are remote.

    Confirm that when all source-types are remote, nothing is mounted to any container.
    """
    robot_server = ot3_remote_everything.robot_server
    can_server = ot3_remote_everything.can_server
    emulators = ot3_remote_everything.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None
    assert can_server.volumes is None

    for emulator in emulators:
        assert emulator.volumes is None


def test_ot3_remote_everything_build_args(
    ot3_remote_everything: RuntimeComposeFileModel,
    opentrons_head: str,
    ot3_firmware_head: str,
) -> None:
    """Test build args when all source-types are remote.

    Confirm that all build args are using the head of their individual repos.
    """
    robot_server = ot3_remote_everything.robot_server
    can_server = ot3_remote_everything.can_server
    emulators = ot3_remote_everything.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    robot_server_build_args = get_source_code_build_args(robot_server)
    can_server_build_args = get_source_code_build_args(can_server)

    assert RepoToBuildArgMapping.OPENTRONS in robot_server_build_args
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    assert RepoToBuildArgMapping.OPENTRONS in can_server_build_args
    assert can_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    for emulator in emulators:
        emulator_build_args = get_source_code_build_args(emulator)
        assert emulator_build_args is not None
        assert RepoToBuildArgMapping.OT3_FIRMWARE in emulator_build_args
        assert (
            emulator_build_args[RepoToBuildArgMapping.OT3_FIRMWARE] == ot3_firmware_head
        )


def test_ot3_local_source_mounts(ot3_local_source: RuntimeComposeFileModel) -> None:
    """Test mounts when source-type is set to local.

    Confirm that ot3-firmware and entrypoint.sh is mounted to emulator containers.
    Confirm other containers have nothing mounted.
    """
    robot_server = ot3_local_source.robot_server
    can_server = ot3_local_source.can_server
    emulators = ot3_local_source.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None

    assert can_server.volumes is None

    for emulator in emulators:
        assert emulator.volumes is not None
        assert len(emulator.volumes) == 2
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", emulator.volumes)
        assert partial_string_in_mount("ot3-firmware:/ot3-firmware", emulator.volumes)


def test_ot3_local_source_build_args(
    ot3_local_source: RuntimeComposeFileModel,
    opentrons_head: str,
    ot3_firmware_head: str,
) -> None:
    """Test build args when source-type is set to local.

    Confirm that robot-server and can-server have source build args.
    Emulators should not have source build args.
    """
    robot_server = ot3_local_source.robot_server
    can_server = ot3_local_source.can_server
    emulators = ot3_local_source.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    robot_server_build_args = get_source_code_build_args(robot_server)
    can_server_build_args = get_source_code_build_args(can_server)

    assert RepoToBuildArgMapping.OPENTRONS in robot_server_build_args
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    assert RepoToBuildArgMapping.OPENTRONS in can_server_build_args
    assert can_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    for emulator in emulators:
        assert build_args_are_none(emulator)


def test_ot3_local_can_server_mounts(ot3_local_can: RuntimeComposeFileModel) -> None:
    """Test mounts when can-server-source-type is set to local.

    Confirm that robot server and emulators have no mounts.
    Confirm that can-server has opentrons and entrypoint.sh mounted in.
    """
    robot_server = ot3_local_can.robot_server
    can_server = ot3_local_can.can_server
    emulators = ot3_local_can.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None

    assert partial_string_in_mount("opentrons:/opentrons", can_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", can_server.volumes)
    assert can_server.volumes is not None
    assert len(can_server.volumes) == 2

    assert ot3_local_can.ot3_emulators is not None
    for emulator in ot3_local_can.ot3_emulators:
        assert emulator.volumes is None


def test_ot3_local_can_server_build_args(
    ot3_local_can: RuntimeComposeFileModel, opentrons_head: str, ot3_firmware_head: str
) -> None:
    """Test build arguments when can-server-source-type is set to local.

    Confirm that can server does not have any build arguments.
    Confirm that robot-server is looking for the opentrons repo head.
    Confirm that the emulators are looking for the ot3-firmware repo head.
    """
    robot_server = ot3_local_can.robot_server
    can_server = ot3_local_can.can_server
    emulators = ot3_local_can.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    robot_server_build_args = get_source_code_build_args(robot_server)

    assert RepoToBuildArgMapping.OPENTRONS in robot_server_build_args
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    assert build_args_are_none(can_server)

    for emulator in emulators:
        emulator_build_args = get_source_code_build_args(emulator)
        assert emulator_build_args is not None
        assert RepoToBuildArgMapping.OT3_FIRMWARE in emulator_build_args
        assert (
            emulator_build_args[RepoToBuildArgMapping.OT3_FIRMWARE] == ot3_firmware_head
        )


def test_ot3_local_robot_server_mounts(
    ot3_local_robot: RuntimeComposeFileModel,
) -> None:
    """Test mounts when robot-server-source-type is set to local.

    Confirm that can server and emulators have no mounts.
    Confirm that robot server has opentrons and entrypoint.sh mounted in.
    """
    robot_server = ot3_local_robot.robot_server
    can_server = ot3_local_robot.can_server
    emulators = ot3_local_robot.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is not None
    assert partial_string_in_mount("opentrons:/opentrons", robot_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server.volumes)
    assert len(robot_server.volumes) == 2

    assert can_server.volumes is None

    assert ot3_local_robot.ot3_emulators is not None
    for emulator in ot3_local_robot.ot3_emulators:
        assert emulator.volumes is None


def test_ot3_local_robot_server_build_args(
    ot3_local_robot: RuntimeComposeFileModel,
    opentrons_head: str,
    ot3_firmware_head: str,
) -> None:
    """Test build arguments when robot-server-source-type is set to local.

    Confirm that robot server does not have any build arguments.
    Confirm that can server is looking for the opentrons repo head.
    Confirm that the emulators are looking for the ot3-firmware repo head.
    """
    robot_server = ot3_local_robot.robot_server
    can_server = ot3_local_robot.can_server
    emulators = ot3_local_robot.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    can_server_build_args = get_source_code_build_args(can_server)

    assert build_args_are_none(robot_server)

    assert RepoToBuildArgMapping.OPENTRONS in can_server_build_args
    assert can_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    for emulator in emulators:
        emulator_build_args = get_source_code_build_args(emulator)
        assert emulator_build_args is not None
        assert RepoToBuildArgMapping.OT3_FIRMWARE in emulator_build_args
        assert (
            emulator_build_args[RepoToBuildArgMapping.OT3_FIRMWARE] == ot3_firmware_head
        )


def test_ot2_remote_everything_mounts(
    ot2_remote_everything: RuntimeComposeFileModel,
) -> None:
    """Test mounts when all source-types are remote.

    Confirm that smoothie and robot server have no mounts.
    """
    robot_server = ot2_remote_everything.robot_server
    smoothie = ot2_remote_everything.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert robot_server.volumes is None
    assert smoothie.volumes is None


def test_ot2_remote_everything_build_args(
    ot2_remote_everything: RuntimeComposeFileModel, opentrons_head: str
) -> None:
    """Test build arguments when all source-types are remote.

    Confirm that smoothie and robot server are both looking for the opentrons repo head.
    """
    robot_server = ot2_remote_everything.robot_server
    smoothie = ot2_remote_everything.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    robot_server_build_args = get_source_code_build_args(robot_server)
    assert robot_server_build_args is not None
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head
    smoothie_build_args = get_source_code_build_args(smoothie)
    assert smoothie_build_args is not None
    assert smoothie_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head


def test_ot2_local_robot_server_mounts(
    ot2_local_robot: RuntimeComposeFileModel,
) -> None:
    """Test mounts when robot-server-source-type is set to local.

    Confirm that robot server has opentrons and entrypoint.sh mounted to it.
    Confirm that smoothie has nothing mounted to it.
    """
    robot_server = ot2_local_robot.robot_server
    smoothie = ot2_local_robot.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert robot_server.volumes is not None
    assert partial_string_in_mount("opentrons:/opentrons", robot_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server.volumes)
    assert len(robot_server.volumes) == 2

    assert smoothie.volumes is None


def test_ot2_local_robot_server_build_args(
    ot2_local_robot: RuntimeComposeFileModel, opentrons_head: str
) -> None:
    """Test build-args when robot-server-source-type is set to local.

    Confirm that robot server has no build arguments
    Confirm that smoothie is looking for the opentrons repo head.
    """
    robot_server = ot2_local_robot.robot_server
    smoothie = ot2_local_robot.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert build_args_are_none(robot_server)

    smoothie_build_args = get_source_code_build_args(smoothie)
    assert smoothie_build_args is not None
    assert smoothie_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head


def test_ot2_local_source_mounts(ot2_local_source: RuntimeComposeFileModel) -> None:
    """Test mounts when source-type is set to local.

    Confirm that robot server has nothing mounted to it.
    Confirm that smoothie has opentrons and entrypoint.sh mounted to it.
    """
    robot_server = ot2_local_source.robot_server
    smoothie = ot2_local_source.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert smoothie.volumes is not None
    assert partial_string_in_mount("opentrons:/opentrons", smoothie.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", smoothie.volumes)
    assert len(smoothie.volumes) == 2

    assert robot_server.volumes is None


def test_ot2_local_source_build_args(
    ot2_local_source: RuntimeComposeFileModel, opentrons_head: str
) -> None:
    """Test build arguments when source-type is set to local.

    Confirm that robot server is looking for the opentrons repo head.
    Confirm that smoothie has no build arguments.
    """
    robot_server = ot2_local_source.robot_server
    smoothie = ot2_local_source.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert robot_server is not None
    assert smoothie is not None

    robot_server_build_args = get_source_code_build_args(robot_server)
    assert robot_server_build_args is not None
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    assert build_args_are_none(smoothie)
