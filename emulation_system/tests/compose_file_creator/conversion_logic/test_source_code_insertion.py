"""Test everything around inserting source code into containers."""
from typing import Any, Dict

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.consts import (
    DEFAULT_ENTRYPOINT_NAME,
    LOCAL_OT3_FIRMWARE_BUILDER_SCRIPT_NAME,
)
from tests.compose_file_creator.conversion_logic.conftest import (
    build_args_are_none,
    check_correct_number_of_volumes,
    get_source_code_build_args,
    mount_string_is,
    partial_string_in_mount,
)
from tests.conftest import get_test_conf


def has_repo_build_args(
    container: Service, monorepo: bool, ot3_firmware: bool, opentrons_modules: bool
) -> bool:
    monorepo_edge = get_test_conf().get_repo_head(OpentronsRepository.OPENTRONS)
    ot3_firmware_edge = get_test_conf().get_repo_head(OpentronsRepository.OT3_FIRMWARE)
    opentrons_modules_edge = get_test_conf().get_repo_head(
        OpentronsRepository.OPENTRONS_MODULES
    )
    build_args = get_source_code_build_args(container)

    if not monorepo and not ot3_firmware and not opentrons_modules:
        return build_args is None

    has_monorepo = monorepo == (
        RepoToBuildArgMapping.OPENTRONS in build_args
        and build_args[RepoToBuildArgMapping.OPENTRONS] == monorepo_edge
    )

    has_ot3_firmware = ot3_firmware == (
        RepoToBuildArgMapping.OT3_FIRMWARE in build_args
        and build_args[RepoToBuildArgMapping.OT3_FIRMWARE] == ot3_firmware_edge
    )

    has_opentrons_modules = opentrons_modules == (
        RepoToBuildArgMapping.OPENTRONS_MODULES in build_args
        and build_args[RepoToBuildArgMapping.OPENTRONS_MODULES]
        == opentrons_modules_edge
    )

    return all([has_monorepo, has_ot3_firmware, has_opentrons_modules])


def test_ot3_remote_everything(
    ot3_remote_everything_latest: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts when all source-types are remote.

    Confirm that when all source-types are remote, nothing is mounted to any container.
    """
    config_file = convert_from_obj(
        ot3_remote_everything_latest, testing_global_em_config, False
    )

    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators
    state_manager = config_file.ot3_state_manager
    assert config_file.local_ot3_firmware_builder is None

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None
    assert state_manager is not None

    assert has_repo_build_args(
        robot_server, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )
    assert has_repo_build_args(
        can_server, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )
    assert has_repo_build_args(
        state_manager, monorepo=True, ot3_firmware=True, opentrons_modules=False
    )

    check_correct_number_of_volumes(robot_server, 0)
    check_correct_number_of_volumes(can_server, 0)
    check_correct_number_of_volumes(state_manager, 0)

    for emulator in emulators:
        check_correct_number_of_volumes(emulator, 0)
        assert has_repo_build_args(
            emulator, monorepo=True, ot3_firmware=True, opentrons_modules=False
        )


def test_ot3_local_source(
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
    state_manager = config_file.ot3_state_manager
    local_ot3_firmware_builder = config_file.local_ot3_firmware_builder

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None
    assert state_manager is not None
    assert local_ot3_firmware_builder is not None

    assert has_repo_build_args(
        robot_server, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )
    assert has_repo_build_args(
        can_server, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )
    assert has_repo_build_args(
        state_manager, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )

    check_correct_number_of_volumes(robot_server, 0)
    check_correct_number_of_volumes(can_server, 0)

    assert partial_string_in_mount("ot3-firmware:/ot3-firmware", state_manager)

    check_correct_number_of_volumes(local_ot3_firmware_builder, 8)
    assert mount_string_is(
        "pipettes_executable:/volumes/pipettes_volume/", local_ot3_firmware_builder
    )
    assert mount_string_is(
        "head_executable:/volumes/head_volume/", local_ot3_firmware_builder
    )
    assert mount_string_is(
        "gantry_x_executable:/volumes/gantry_x_volume/", local_ot3_firmware_builder
    )
    assert mount_string_is(
        "gantry_y_executable:/volumes/gantry_y_volume/", local_ot3_firmware_builder
    )
    assert mount_string_is(
        "bootloader_executable:/volumes/bootloader_volume/", local_ot3_firmware_builder
    )
    assert mount_string_is(
        "gripper_executable:/volumes/gripper_volume/", local_ot3_firmware_builder
    )
    assert partial_string_in_mount(
        "local_ot3_firmware_builder.sh:/local_ot3_firmware_builder.sh",
        local_ot3_firmware_builder,
    )
    assert partial_string_in_mount(
        "ot3-firmware:/ot3-firmware", local_ot3_firmware_builder
    )
    assert has_repo_build_args(
        local_ot3_firmware_builder,
        monorepo=True,
        ot3_firmware=False,
        opentrons_modules=False,
    )

    for emulator in emulators:
        check_correct_number_of_volumes(emulator, 3)
        assert partial_string_in_mount(
            f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", emulator
        )
        assert partial_string_in_mount("ot3-firmware:/ot3-firmware", emulator)
        assert partial_string_in_mount("executable:/executable", emulator)
        assert has_repo_build_args(
            emulator, monorepo=True, ot3_firmware=False, opentrons_modules=False
        )


def test_ot3_local_can_server(
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
    state_manager = config_file.ot3_state_manager
    assert config_file.local_ot3_firmware_builder is None

    assert robot_server is not None
    assert can_server is not None
    assert state_manager is not None
    assert emulators is not None

    assert has_repo_build_args(
        robot_server, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )
    assert has_repo_build_args(
        can_server, monorepo=False, ot3_firmware=False, opentrons_modules=False
    )
    assert has_repo_build_args(
        state_manager, monorepo=True, ot3_firmware=True, opentrons_modules=False
    )

    check_correct_number_of_volumes(state_manager, 0)
    check_correct_number_of_volumes(robot_server, 0)

    check_correct_number_of_volumes(can_server, 3)
    assert partial_string_in_mount("opentrons:/opentrons", can_server)
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", can_server
    )
    assert partial_string_in_mount("opentrons-python-dist:/dist", can_server)

    for emulator in emulators:
        check_correct_number_of_volumes(emulator, 0)
        assert has_repo_build_args(
            state_manager, monorepo=True, ot3_firmware=True, opentrons_modules=False
        )


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
    state_manager = config_file.ot3_state_manager
    assert config_file.local_ot3_firmware_builder is None

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None
    assert state_manager is not None

    check_correct_number_of_volumes(robot_server, 3)
    assert partial_string_in_mount("opentrons:/opentrons", robot_server)
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", robot_server
    )
    assert partial_string_in_mount("opentrons-python-dist:/dist", robot_server)
    assert has_repo_build_args(
        robot_server, monorepo=False, ot3_firmware=False, opentrons_modules=False
    )

    check_correct_number_of_volumes(can_server, 0)
    assert has_repo_build_args(
        can_server, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )

    check_correct_number_of_volumes(state_manager, 0)
    assert has_repo_build_args(
        state_manager, monorepo=True, ot3_firmware=True, opentrons_modules=False
    )

    for emulator in config_file.ot3_emulators:
        check_correct_number_of_volumes(emulator, 0)
        assert has_repo_build_args(
            state_manager, monorepo=True, ot3_firmware=True, opentrons_modules=False
        )


def test_ot3_local_opentrons_hardware(
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
    state_manager = config_file.ot3_state_manager
    local_ot3_firmware_builder = config_file.local_ot3_firmware_builder

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None
    assert state_manager is not None
    assert local_ot3_firmware_builder is not None

    check_correct_number_of_volumes(robot_server, 0)
    assert has_repo_build_args(
        robot_server, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )

    check_correct_number_of_volumes(can_server, 0)
    assert has_repo_build_args(
        can_server, monorepo=True, ot3_firmware=False, opentrons_modules=False
    )

    check_correct_number_of_volumes(state_manager, 2)
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", state_manager
    )
    assert partial_string_in_mount(
        "state_manager_venv:/ot3-firmware/build-host/.venv", state_manager
    )
    assert has_repo_build_args(
        state_manager, monorepo=False, ot3_firmware=True, opentrons_modules=False
    )

    check_correct_number_of_volumes(
        local_ot3_firmware_builder, 3
    ), f"Correct number of volumes is "
    assert partial_string_in_mount(
        f"{LOCAL_OT3_FIRMWARE_BUILDER_SCRIPT_NAME}:/{LOCAL_OT3_FIRMWARE_BUILDER_SCRIPT_NAME}",
        local_ot3_firmware_builder,
    )
    assert partial_string_in_mount(
        "state_manager_venv:/ot3-firmware/build-host/.venv", local_ot3_firmware_builder
    )
    assert partial_string_in_mount("opentrons:/opentrons", local_ot3_firmware_builder)
    has_repo_build_args(
        local_ot3_firmware_builder,
        monorepo=False,
        ot3_firmware=True,
        opentrons_modules=False,
    )

    for emulator in emulators:
        check_correct_number_of_volumes(emulator, 2)
        assert partial_string_in_mount(
            f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", emulator
        )
        assert partial_string_in_mount("opentrons:/opentrons", emulator)
        has_repo_build_args(
            emulator, monorepo=False, ot3_firmware=True, opentrons_modules=False
        )


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
    assert partial_string_in_mount("opentrons:/opentrons", smoothie)
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", smoothie
    )
    assert partial_string_in_mount("opentrons-python-dist:/dist", smoothie)

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
    assert partial_string_in_mount("opentrons:/opentrons", robot_server)
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", robot_server
    )
    assert partial_string_in_mount("opentrons-python-dist:/dist", robot_server)
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
        "opentrons-modules:/opentrons-modules", heater_shaker
    )
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", heater_shaker
    )
    assert partial_string_in_mount(
        "opentrons-modules-build-stm32-host:/opentrons-modules/build-stm32-host",
        heater_shaker,
    )
    assert partial_string_in_mount(
        "opentrons-modules-stm32-tools:/opentrons-modules/stm32-tools",
        heater_shaker,
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
        "opentrons-modules:/opentrons-modules", thermocycler_module
    )
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", thermocycler_module
    )
    assert partial_string_in_mount(
        "opentrons-modules-build-stm32-host:/opentrons-modules/build-stm32-host",
        thermocycler_module,
    )
    assert partial_string_in_mount(
        "opentrons-modules-stm32-tools:/opentrons-modules/stm32-tools",
        thermocycler_module,
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

    assert partial_string_in_mount("opentrons:/opentrons", thermocycler_module)
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", thermocycler_module
    )
    assert partial_string_in_mount("opentrons-python-dist:/dist", thermocycler_module)

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

    assert partial_string_in_mount("opentrons:/opentrons", temperature_module)
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", temperature_module
    )
    assert partial_string_in_mount("opentrons-python-dist:/dist", temperature_module)

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

    assert partial_string_in_mount("opentrons:/opentrons", magnetic_module)
    assert partial_string_in_mount(
        f"{DEFAULT_ENTRYPOINT_NAME}:/{DEFAULT_ENTRYPOINT_NAME}", magnetic_module
    )
    assert partial_string_in_mount("opentrons-python-dist:/dist", magnetic_module)

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
