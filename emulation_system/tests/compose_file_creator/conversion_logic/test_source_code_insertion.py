"""Test everything around inserting source code into containers."""
from typing import Any, Dict

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from tests.compose_file_creator.conversion_logic.conftest import (
    build_args_are_none,
    get_source_code_build_args,
    partial_string_in_mount,
)


@pytest.mark.parametrize(
    "config_dict",
    [
        lazy_fixture("ot3_remote_everything_latest"),
        lazy_fixture("ot3_remote_everything_commit_id"),
    ],
)
def test_ot3_remote_everything_mounts(
    config_dict: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when all source-types are remote.

    Confirm that when all source-types are remote, nothing is mounted to any container.
    """
    config_file = convert_from_obj(config_dict, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None
    assert can_server.volumes is None

    for emulator in emulators:
        assert emulator.volumes is None


def test_ot3_remote_everything_latest_build_args(
    ot3_remote_everything_latest: Dict[str, Any],
    opentrons_head: str,
    ot3_firmware_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build args when all source-types are remote latest.

    Confirm that all build args are using the head of their individual repos.
    """
    config_file = convert_from_obj(
        ot3_remote_everything_latest, testing_global_em_config, False
    )
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

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
        assert RepoToBuildArgMapping.OPENTRONS in emulator_build_args
        assert emulator_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head


def test_ot3_remote_everything_commit_id_build_args(
    ot3_remote_everything_commit_id: Dict[str, Any],
    opentrons_commit: str,
    ot3_firmware_commit: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build args when all source-types are remote commit id.

    Confirm that all build args are using the head of their individual repos.
    """
    config_file = convert_from_obj(
        ot3_remote_everything_commit_id, testing_global_em_config, False
    )
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    robot_server_build_args = get_source_code_build_args(robot_server)
    can_server_build_args = get_source_code_build_args(can_server)

    assert RepoToBuildArgMapping.OPENTRONS in robot_server_build_args
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_commit

    assert RepoToBuildArgMapping.OPENTRONS in can_server_build_args
    assert can_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_commit

    for emulator in emulators:
        emulator_build_args = get_source_code_build_args(emulator)
        assert emulator_build_args is not None
        assert RepoToBuildArgMapping.OT3_FIRMWARE in emulator_build_args
        assert (
            emulator_build_args[RepoToBuildArgMapping.OT3_FIRMWARE]
            == ot3_firmware_commit
        )
        assert RepoToBuildArgMapping.OPENTRONS in emulator_build_args
        assert emulator_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_commit


def test_ot3_local_source_mounts(
    ot3_local_source: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that ot3-firmware and entrypoint.sh is mounted to emulator containers.
    Confirm other containers have nothing mounted.
    """
    config_file = convert_from_obj(ot3_local_source, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None

    assert can_server.volumes is None

    for emulator in emulators:
        assert emulator.volumes is not None
        assert len(emulator.volumes) == 4
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", emulator.volumes)
        assert partial_string_in_mount("ot3-firmware:/ot3-firmware", emulator.volumes)
        assert partial_string_in_mount(
            "stm32-tools:/ot3-firmware/stm32-tools", emulator.volumes
        )
        assert partial_string_in_mount(
            "build-host:/ot3-firmware/build-host", emulator.volumes
        )


def test_ot3_local_source_build_args(
    ot3_local_source: Dict[str, Any],
    opentrons_head: str,
    ot3_firmware_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build args when source-type is set to local.

    Confirm that robot-server and can-server have source build args.
    Emulators should not have source build args.
    """
    config_file = convert_from_obj(ot3_local_source, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

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
        assert RepoToBuildArgMapping.OPENTRONS in emulator_build_args
        assert emulator_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head
        assert RepoToBuildArgMapping.OT3_FIRMWARE not in emulator_build_args


def test_ot3_local_can_server_mounts(
    ot3_local_can: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when can-server-source-type is set to local.

    Confirm that robot server and emulators have no mounts.
    Confirm that can-server has opentrons and entrypoint.sh mounted in.
    """
    config_file = convert_from_obj(ot3_local_can, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None
    assert can_server.volumes is not None

    assert partial_string_in_mount("opentrons:/opentrons", can_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", can_server.volumes)
    assert partial_string_in_mount("opentrons-python-dist:/dist", can_server.volumes)

    assert len(can_server.volumes) == 3

    assert config_file.ot3_emulators is not None
    for emulator in config_file.ot3_emulators:
        assert emulator.volumes is None


def test_ot3_local_can_server_build_args(
    ot3_local_can: Dict[str, Any],
    opentrons_head: str,
    ot3_firmware_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build arguments when can-server-source-type is set to local.

    Confirm that can server does not have any build arguments.
    Confirm that robot-server is looking for the opentrons repo head.
    Confirm that the emulators are looking for the ot3-firmware repo head.
    """
    config_file = convert_from_obj(ot3_local_can, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    robot_server_build_args = get_source_code_build_args(robot_server)

    assert RepoToBuildArgMapping.OPENTRONS in robot_server_build_args
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    assert build_args_are_none(can_server)

    for emulator in emulators:
        print(emulator.container_name)
        emulator_build_args = get_source_code_build_args(emulator)
        assert emulator_build_args is not None
        assert RepoToBuildArgMapping.OT3_FIRMWARE in emulator_build_args
        assert (
            emulator_build_args[RepoToBuildArgMapping.OT3_FIRMWARE] == ot3_firmware_head
        )
        assert RepoToBuildArgMapping.OPENTRONS in emulator_build_args
        assert emulator_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head


def test_ot3_local_robot_server_mounts(
    ot3_local_robot: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when robot-server-source-type is set to local.

    Confirm that can server and emulators have no mounts.
    Confirm that robot server has opentrons and entrypoint.sh mounted in.
    """
    config_file = convert_from_obj(ot3_local_robot, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is not None
    assert partial_string_in_mount("opentrons:/opentrons", robot_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server.volumes)
    assert partial_string_in_mount("opentrons-python-dist:/dist", robot_server.volumes)

    assert len(robot_server.volumes) == 3

    assert can_server.volumes is None

    assert config_file.ot3_emulators is not None
    for emulator in config_file.ot3_emulators:
        assert emulator.volumes is None


def test_ot3_local_robot_server_build_args(
    ot3_local_robot: Dict[str, Any],
    opentrons_head: str,
    ot3_firmware_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build arguments when robot-server-source-type is set to local.

    Confirm that robot server does not have any build arguments.
    Confirm that can server is looking for the opentrons repo head.
    Confirm that the emulators are looking for the ot3-firmware repo head.
    """
    config_file = convert_from_obj(ot3_local_robot, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

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
        assert RepoToBuildArgMapping.OPENTRONS in emulator_build_args
        assert emulator_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head


def test_ot3_local_opentrons_hardware_build_args(
    ot3_local_opentrons_hardware: Dict[str, Any],
    opentrons_head: str,
    ot3_firmware_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build arguments when robot-server-source-type is set to local.

    Confirm that robot server does not have any build arguments.
    Confirm that can server is looking for the opentrons repo head.
    Confirm that the emulators are looking for the ot3-firmware repo head.
    """
    config_file = convert_from_obj(
        ot3_local_opentrons_hardware, testing_global_em_config, False
    )
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    can_server_build_args = get_source_code_build_args(can_server)
    robot_server_build_args = get_source_code_build_args(robot_server)

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
        assert RepoToBuildArgMapping.OPENTRONS not in emulator_build_args


def test_ot3_local_opentrons_hardware_mounts(
    ot3_local_opentrons_hardware: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when robot-server-source-type is set to local.

    Confirm that can server and emulators have no mounts.
    Confirm that robot server has opentrons and entrypoint.sh mounted in.
    """
    config_file = convert_from_obj(
        ot3_local_opentrons_hardware, testing_global_em_config, False
    )
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None

    assert robot_server.volumes is None

    assert can_server.volumes is None

    assert config_file.ot3_emulators is not None

    for emulator in config_file.ot3_emulators:
        assert emulator.volumes is not None
        assert len(emulator.volumes) == 3
        assert partial_string_in_mount("opentrons:/opentrons", emulator.volumes)
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", emulator.volumes)
        assert partial_string_in_mount("opentrons-python-dist:/dist", emulator.volumes)


@pytest.mark.parametrize(
    "config_dict",
    [
        lazy_fixture("ot2_remote_everything_latest"),
        lazy_fixture("ot2_remote_everything_commit_id"),
    ],
)
def test_ot2_remote_everything_mounts(
    config_dict: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when all source-types are remote.

    Confirm that smoothie and robot server have no mounts.
    """
    config_file = convert_from_obj(config_dict, testing_global_em_config, False)
    robot_server = config_file.robot_server
    smoothie = config_file.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert robot_server.volumes is None
    assert smoothie.volumes is None


def test_ot2_remote_everything_latest_build_args(
    ot2_remote_everything_latest: Dict[str, Any],
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build arguments when all source-types are remote latest.

    Confirm that smoothie and robot server are both looking for the opentrons repo head.
    """
    config_file = convert_from_obj(
        ot2_remote_everything_latest, testing_global_em_config, False
    )
    robot_server = config_file.robot_server
    smoothie = config_file.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    robot_server_build_args = get_source_code_build_args(robot_server)
    assert robot_server_build_args is not None
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head
    smoothie_build_args = get_source_code_build_args(smoothie)
    assert smoothie_build_args is not None
    assert smoothie_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head


def test_ot2_remote_everything_commit_id_build_args(
    ot2_remote_everything_commit_id: Dict[str, Any],
    opentrons_commit: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build arguments when all source-types are remote commit id.

    Confirm that smoothie and robot server are both looking for the opentrons repo head.
    """
    config_file = convert_from_obj(
        ot2_remote_everything_commit_id, testing_global_em_config, False
    )
    robot_server = config_file.robot_server
    smoothie = config_file.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    robot_server_build_args = get_source_code_build_args(robot_server)
    assert robot_server_build_args is not None
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_commit

    smoothie_build_args = get_source_code_build_args(smoothie)
    assert smoothie_build_args is not None
    assert smoothie_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_commit


def test_ot2_local_source_mounts(
    ot2_local_source: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that robot server has nothing mounted to it.
    Confirm that smoothie has opentrons and entrypoint.sh mounted to it.
    """
    config_file = convert_from_obj(ot2_local_source, testing_global_em_config, False)
    robot_server = config_file.robot_server
    smoothie = config_file.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert smoothie.volumes is not None
    assert partial_string_in_mount("opentrons:/opentrons", smoothie.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", smoothie.volumes)
    assert partial_string_in_mount("opentrons-python-dist:/dist", smoothie.volumes)

    assert len(smoothie.volumes) == 3

    assert robot_server.volumes is None


def test_ot2_local_source_build_args(
    ot2_local_source: Dict[str, Any],
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build arguments when source-type is set to local.

    Confirm that robot server is looking for the opentrons repo head.
    Confirm that smoothie has no build arguments.
    """
    config_file = convert_from_obj(ot2_local_source, testing_global_em_config, False)
    robot_server = config_file.robot_server
    smoothie = config_file.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert robot_server is not None
    assert smoothie is not None

    robot_server_build_args = get_source_code_build_args(robot_server)
    assert robot_server_build_args is not None
    assert robot_server_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head

    assert build_args_are_none(smoothie)


def test_ot2_local_robot_server_mounts(
    ot2_local_robot: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when robot-server-source-type is set to local.

    Confirm that robot server has opentrons and entrypoint.sh mounted to it.
    Confirm that smoothie has nothing mounted to it.
    """
    config_file = convert_from_obj(ot2_local_robot, testing_global_em_config, False)
    robot_server = config_file.robot_server
    smoothie = config_file.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert robot_server.volumes is not None
    assert partial_string_in_mount("opentrons:/opentrons", robot_server.volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server.volumes)
    assert partial_string_in_mount("opentrons-python-dist:/dist", robot_server.volumes)
    assert len(robot_server.volumes) == 3

    assert smoothie.volumes is None


def test_ot2_local_robot_server_build_args(
    ot2_local_robot: Dict[str, Any],
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test build-args when robot-server-source-type is set to local.

    Confirm that robot server has no build arguments
    Confirm that smoothie is looking for the opentrons repo head.
    """
    config_file = convert_from_obj(ot2_local_robot, testing_global_em_config, False)
    robot_server = config_file.robot_server
    smoothie = config_file.smoothie_emulator

    assert robot_server is not None
    assert smoothie is not None

    assert build_args_are_none(robot_server)

    smoothie_build_args = get_source_code_build_args(smoothie)
    assert smoothie_build_args is not None
    assert smoothie_build_args[RepoToBuildArgMapping.OPENTRONS] == opentrons_head


def test_heater_shaker_hardware_local_mounts(
    heater_shaker_module_hardware_local: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that heater shaker has opentrons-modules, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-modules-build-stm32-host and
    opentrons-modules-stm32-tools exist and are bound to the correct location.
    """
    config_file = convert_from_obj(
        heater_shaker_module_hardware_local, testing_global_em_config, False
    )
    heater_shakers = config_file.heater_shaker_module_emulators

    assert heater_shakers is not None
    assert len(heater_shakers) == 1

    heater_shaker = heater_shakers[0]
    assert heater_shaker.volumes is not None

    assert partial_string_in_mount(
        "opentrons-modules:/opentrons-modules", heater_shaker.volumes
    )
    assert partial_string_in_mount(
        "entrypoint.sh:/entrypoint.sh", heater_shaker.volumes
    )
    assert partial_string_in_mount(
        "opentrons-modules-build-stm32-host:/opentrons-modules/build-stm32-host",
        heater_shaker.volumes,
    )
    assert partial_string_in_mount(
        "opentrons-modules-stm32-tools:/opentrons-modules/stm32-tools",
        heater_shaker.volumes,
    )

    assert len(heater_shaker.volumes) == 4


def test_thermocycler_module_hardware_local_mounts(
    thermocycler_module_hardware_local: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that thermoycler has opentrons-modules, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-modules-build-stm32-host and
    opentrons-modules-stm32-tools exist and are bound to the correct location.
    """
    config_file = convert_from_obj(
        thermocycler_module_hardware_local, testing_global_em_config, False
    )
    thermocycler_modules = config_file.thermocycler_module_emulators

    assert thermocycler_modules is not None
    assert len(thermocycler_modules) == 1

    thermocycler_module = thermocycler_modules[0]
    assert thermocycler_module.volumes is not None

    assert partial_string_in_mount(
        "opentrons-modules:/opentrons-modules", thermocycler_module.volumes
    )
    assert partial_string_in_mount(
        "entrypoint.sh:/entrypoint.sh", thermocycler_module.volumes
    )
    assert partial_string_in_mount(
        "opentrons-modules-build-stm32-host:/opentrons-modules/build-stm32-host",
        thermocycler_module.volumes,
    )
    assert partial_string_in_mount(
        "opentrons-modules-stm32-tools:/opentrons-modules/stm32-tools",
        thermocycler_module.volumes,
    )

    assert len(thermocycler_module.volumes) == 4


def test_thermocycler_module_firmware_local_mounts(
    thermocycler_module_firmware_local: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that thermocycler module has opentrons, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-python-dist bound to the correct
    location.
    """
    config_file = convert_from_obj(
        thermocycler_module_firmware_local, testing_global_em_config, False
    )
    thermocycler_modules = config_file.thermocycler_module_emulators

    assert thermocycler_modules is not None
    assert len(thermocycler_modules) == 1

    thermocycler_module = thermocycler_modules[0]
    assert thermocycler_module.volumes is not None

    assert partial_string_in_mount("opentrons:/opentrons", thermocycler_module.volumes)
    assert partial_string_in_mount(
        "entrypoint.sh:/entrypoint.sh", thermocycler_module.volumes
    )
    assert partial_string_in_mount(
        "opentrons-python-dist:/dist", thermocycler_module.volumes
    )

    assert len(thermocycler_module.volumes) == 3


def test_temperature_module_firmware_local_mounts(
    temperature_module_firmware_local: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that temperature module has opentrons, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-python-dist bound to the correct
    location.
    """
    config_file = convert_from_obj(
        temperature_module_firmware_local, testing_global_em_config, False
    )
    temperature_modules = config_file.temperature_module_emulators

    assert temperature_modules is not None
    assert len(temperature_modules) == 1

    temperature_module = temperature_modules[0]
    assert temperature_module.volumes is not None

    assert partial_string_in_mount("opentrons:/opentrons", temperature_module.volumes)
    assert partial_string_in_mount(
        "entrypoint.sh:/entrypoint.sh", temperature_module.volumes
    )
    assert partial_string_in_mount(
        "opentrons-python-dist:/dist", temperature_module.volumes
    )

    assert len(temperature_module.volumes) == 3


def test_magnetic_module_firmware_local_mounts(
    magnetic_module_firmware_local: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that magnetic module has opentrons, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-python-dist bound to the correct
    location.
    """
    config_file = convert_from_obj(
        magnetic_module_firmware_local, testing_global_em_config, False
    )
    magnetic_modules = config_file.magnetic_module_emulators

    assert magnetic_modules is not None
    assert len(magnetic_modules) == 1

    magnetic_module = magnetic_modules[0]
    assert magnetic_module.volumes is not None

    assert partial_string_in_mount("opentrons:/opentrons", magnetic_module.volumes)
    assert partial_string_in_mount(
        "entrypoint.sh:/entrypoint.sh", magnetic_module.volumes
    )
    assert partial_string_in_mount(
        "opentrons-python-dist:/dist", magnetic_module.volumes
    )

    assert len(magnetic_module.volumes) == 3


def test_heater_shaker_hardware_remote_mounts(
    heater_shaker_module_hardware_remote: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that heater shaker has opentrons-modules, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-modules-build-stm32-host and
    opentrons-modules-stm32-tools exist and are bound to the correct location.
    """
    config_file = convert_from_obj(
        heater_shaker_module_hardware_remote, testing_global_em_config, False
    )
    heater_shakers = config_file.heater_shaker_module_emulators

    assert heater_shakers is not None
    assert len(heater_shakers) == 1

    heater_shaker = heater_shakers[0]
    assert heater_shaker.volumes is None


def test_thermocycler_module_hardware_remote_mounts(
    thermocycler_module_firmware_remote: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to remote.

    Confirm that there are no mounts
    """
    config_file = convert_from_obj(
        thermocycler_module_firmware_remote, testing_global_em_config, False
    )
    thermocycler_modules = config_file.thermocycler_module_emulators

    assert thermocycler_modules is not None
    assert len(thermocycler_modules) == 1

    thermocycler_module = thermocycler_modules[0]
    assert thermocycler_module.volumes is None


def test_temperature_module_firmware_remote_mounts(
    temperature_module_firmware_remote: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that temperature module has opentrons, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-python-dist bound to the correct
    location.
    """
    config_file = convert_from_obj(
        temperature_module_firmware_remote, testing_global_em_config, False
    )
    temperature_modules = config_file.temperature_module_emulators

    assert temperature_modules is not None
    assert len(temperature_modules) == 1

    temperature_module = temperature_modules[0]
    assert temperature_module.volumes is None


def test_magnetic_module_firmware_remote_mounts(
    magnetic_module_firmware_remote: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that magnetic module has opentrons, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-python-dist bound to the correct
    location.
    """
    config_file = convert_from_obj(
        magnetic_module_firmware_remote, testing_global_em_config, False
    )
    magnetic_modules = config_file.magnetic_module_emulators

    assert magnetic_modules is not None
    assert len(magnetic_modules) == 1

    magnetic_module = magnetic_modules[0]
    assert magnetic_module.volumes is None


def test_thermocycler_module_firmware_remote_mounts(
    thermocycler_module_firmware_remote: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when source-type is set to local.

    Confirm that thermocycler module has opentrons, entrypoint.sh mounted in.
    Also confirm that named volumes: opentrons-python-dist bound to the correct
    location.
    """
    config_file = convert_from_obj(
        thermocycler_module_firmware_remote, testing_global_em_config, False
    )
    thermocycler_modules = config_file.thermocycler_module_emulators

    assert thermocycler_modules is not None
    assert len(thermocycler_modules) == 1

    thermocycler_module = thermocycler_modules[0]
    assert thermocycler_module.volumes is None


@pytest.mark.parametrize(
    "config_dict",
    [
        lazy_fixture("ot3_remote_everything_latest"),
        lazy_fixture("ot3_remote_everything_commit_id"),
        lazy_fixture("ot2_remote_everything_latest"),
        lazy_fixture("ot2_remote_everything_commit_id"),
    ],
)
def test_is_remote(
    config_dict: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm that when all source-types are remote, is_remote is True."""
    config_file = convert_from_obj(config_dict, testing_global_em_config, False)
    assert config_file.is_remote


@pytest.mark.parametrize(
    "config_dict",
    [
        lazy_fixture("ot3_local_robot"),
        lazy_fixture("ot3_local_source"),
        lazy_fixture("ot3_local_can"),
        lazy_fixture("ot2_local_source"),
        lazy_fixture("ot2_local_robot"),
    ],
)
def test_is_not_remote(
    config_dict: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm that when all source-types are not remote, is_remote is False."""
    config_file = convert_from_obj(config_dict, testing_global_em_config, False)
    assert not config_file.is_remote
