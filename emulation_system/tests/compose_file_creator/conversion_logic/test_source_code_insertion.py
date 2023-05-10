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
from tests.validation_helper_functions import (
    build_args_are_none,
    check_correct_number_of_volumes,
    get_source_code_build_args,
    partial_string_in_mount,
)


@pytest.mark.parametrize(
    "config, monorepo_is_local, ot3_firmware_is_local",
    [
        [lazy_fixture("ot3_only"), False, False],
        [lazy_fixture("ot3_and_modules"), False, False],
        [lazy_fixture("ot3_remote_everything_commit_id"), False, False],
        [lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"), False, True],
        [lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"), True, False],
        [lazy_fixture("ot3_local_everything"), True, True],
    ],
)
def test_ot3_build_args(
    config: Dict[str, Any],
    monorepo_is_local: bool,
    ot3_firmware_is_local: bool,
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm build args are created correctly for OT-3."""
    config_file = convert_from_obj(config, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators
    ot3_firmware_builder = config_file.ot3_firmware_builder
    monorepo_builder = config_file.monorepo_builder
    state_manager = config_file.ot3_state_manager

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None
    assert ot3_firmware_builder is not None
    assert monorepo_builder is not None
    assert state_manager is not None

    assert build_args_are_none(robot_server)
    assert build_args_are_none(can_server)
    assert all(build_args_are_none(emulator) for emulator in emulators)
    assert build_args_are_none(state_manager)

    if monorepo_is_local and ot3_firmware_is_local:
        assert build_args_are_none(ot3_firmware_builder)
    else:

        num_local_ot3_firmware_build_args = 0

        build_args = get_source_code_build_args(ot3_firmware_builder)
        assert build_args is not None
        assert RepoToBuildArgMapping.OPENTRONS_MODULES not in build_args

        if not monorepo_is_local:
            num_local_ot3_firmware_build_args += 1
            assert RepoToBuildArgMapping.OPENTRONS in build_args
        else:
            assert RepoToBuildArgMapping.OPENTRONS not in build_args

        if not ot3_firmware_is_local:
            num_local_ot3_firmware_build_args += 1
            assert RepoToBuildArgMapping.OT3_FIRMWARE in build_args
        else:
            assert RepoToBuildArgMapping.OT3_FIRMWARE not in build_args

        assert len(build_args) == num_local_ot3_firmware_build_args

    if monorepo_is_local:
        assert build_args_are_none(monorepo_builder)
    else:
        build_args = get_source_code_build_args(monorepo_builder)
        assert build_args is not None
        assert len(build_args) == 1
        assert RepoToBuildArgMapping.OPENTRONS in build_args


@pytest.mark.parametrize(
    "config, monorepo_is_local",
    [
        [lazy_fixture("ot2_only"), False],
        [lazy_fixture("ot2_and_modules"), False],
        [lazy_fixture("ot2_remote_everything_commit_id"), False],
        [lazy_fixture("ot2_local_source"), True],
    ],
)
def test_ot2_build_args(
    config: Dict[str, Any],
    monorepo_is_local: bool,
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm build args are created correctly for OT-2."""
    config_file = convert_from_obj(config, testing_global_em_config, False)
    robot = config_file.robot_server
    emulator_proxy = config_file.emulator_proxy
    smoothie = config_file.smoothie_emulator
    monorepo_builder = config_file.monorepo_builder

    assert robot is not None
    assert emulator_proxy is not None
    assert smoothie is not None
    assert monorepo_builder is not None

    assert build_args_are_none(robot)
    assert build_args_are_none(emulator_proxy)
    assert build_args_are_none(smoothie)

    if monorepo_is_local:
        assert build_args_are_none(monorepo_builder)
    else:
        build_args = get_source_code_build_args(monorepo_builder)
        assert build_args is not None
        assert len(build_args) == 1
        assert RepoToBuildArgMapping.OPENTRONS in build_args


@pytest.mark.parametrize(
    "config, monorepo_is_local",
    [
        [lazy_fixture("thermocycler_module_firmware_remote"), False],
        [lazy_fixture("thermocycler_module_firmware_local"), True],
        [lazy_fixture("temperature_module_firmware_local"), True],
        [lazy_fixture("temperature_module_firmware_remote"), False],
        [lazy_fixture("magnetic_module_firmware_remote"), False],
        [lazy_fixture("magnetic_module_firmware_local"), True],
        [lazy_fixture("heater_shaker_module_firmware_local"), True],
        [lazy_fixture("heater_shaker_module_firmware_remote"), False],
    ],
)
def test_module_monorepo_build_args(
    config: Dict[str, Any],
    monorepo_is_local: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm build args are created correctly for modules using monorepo."""
    config_file = convert_from_obj(config, testing_global_em_config, False)
    modules = config_file.module_emulators
    monorepo_builder = config_file.monorepo_builder

    assert modules is not None
    assert all(module is not None for module in modules)
    assert monorepo_builder is not None

    assert all(build_args_are_none(module) for module in modules)

    if monorepo_is_local:
        assert build_args_are_none(monorepo_builder)
    else:
        build_args = get_source_code_build_args(monorepo_builder)
        assert build_args is not None
        assert len(build_args) == 1
        assert RepoToBuildArgMapping.OPENTRONS in build_args


@pytest.mark.parametrize(
    "config, opentrons_modules_is_local",
    [
        [lazy_fixture("thermocycler_module_hardware_remote"), False],
        [lazy_fixture("thermocycler_module_hardware_local"), True],
        [lazy_fixture("heater_shaker_module_hardware_local"), True],
        [lazy_fixture("heater_shaker_module_hardware_remote"), False],
    ],
)
def test_module_opentrons_modules_build_args(
    config: Dict[str, Any],
    opentrons_modules_is_local: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm build args are created correctly for modules using opentrons-modules."""
    config_file = convert_from_obj(config, testing_global_em_config, False)
    modules = config_file.module_emulators
    opentrons_modules_builder = config_file.opentrons_modules_builder

    assert modules is not None
    assert all(module is not None for module in modules)
    assert opentrons_modules_builder is not None

    assert all(build_args_are_none(module) for module in modules)

    if opentrons_modules_is_local:
        assert build_args_are_none(opentrons_modules_builder)
    else:
        build_args = get_source_code_build_args(opentrons_modules_builder)
        assert build_args is not None
        assert len(build_args) == 1
        assert RepoToBuildArgMapping.OPENTRONS_MODULES in build_args


@pytest.mark.parametrize(
    "config, monorepo_is_local, ot3_firmware_is_local",
    [
        [lazy_fixture("ot3_only"), False, False],
        [lazy_fixture("ot3_and_modules"), False, False],
        [lazy_fixture("ot3_remote_everything_commit_id"), False, False],
        [lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"), False, True],
        [lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"), True, False],
        [lazy_fixture("ot3_local_everything"), True, True],
    ],
)
def test_ot3_mounts(
    config: Dict[str, Any],
    monorepo_is_local: bool,
    ot3_firmware_is_local: bool,
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts are created correctly when creating an OT-3."""
    config_file = convert_from_obj(config, testing_global_em_config, False)
    robot_server = config_file.robot_server
    can_server = config_file.can_server
    emulators = config_file.ot3_emulators
    ot3_firmware_builder = config_file.ot3_firmware_builder
    monorepo_builder = config_file.monorepo_builder
    state_manager = config_file.ot3_state_manager

    assert robot_server is not None
    assert can_server is not None
    assert emulators is not None
    assert ot3_firmware_builder is not None
    assert monorepo_builder is not None
    assert state_manager is not None

    # robot-server, can-server, and local-monorepo-builder
    # should always have entrypoint.sh and monorepo-wheels
    check_correct_number_of_volumes(robot_server, 2)
    check_correct_number_of_volumes(can_server, 2)
    check_correct_number_of_volumes(state_manager, 4)

    check_correct_number_of_volumes(monorepo_builder, 2 if monorepo_is_local else 1)

    # Firmware builder should have the following volumes:
    # 1 volume per emulator for copying the binaries over
    # State Manager Venv
    # State Manager Wheel
    # build-host cache override
    # stm32-tools cache override

    check_correct_number_of_volumes(
        ot3_firmware_builder, len(emulators) + (5 if ot3_firmware_is_local else 4)
    )

    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot_server)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", can_server)
    assert partial_string_in_mount("monorepo-wheels:/dist", robot_server)
    assert partial_string_in_mount("monorepo-wheels:/dist", can_server)
    assert partial_string_in_mount("monorepo-wheels:/dist", monorepo_builder)

    if monorepo_is_local:
        assert partial_string_in_mount("/opentrons:/opentrons", monorepo_builder)

    if ot3_firmware_is_local:
        assert partial_string_in_mount(
            "/ot3-firmware:/ot3-firmware", ot3_firmware_builder
        )

    for emulator in emulators:
        check_correct_number_of_volumes(emulator, 2)
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", emulator)
        assert emulator.image is not None
        hardware_name = emulator.image.replace("ot3-", "").replace("-hardware", "")

        assert partial_string_in_mount(
            f"{hardware_name}-executable:/executable", emulator
        )

        # Note checking volumes on ot3_firmware_builder here
        assert partial_string_in_mount(
            f"{hardware_name}-executable:/volumes/{hardware_name}-volume",
            ot3_firmware_builder,
        )


@pytest.mark.parametrize(
    "config, monorepo_is_local",
    [
        [lazy_fixture("ot2_only"), False],
        [lazy_fixture("ot2_and_modules"), False],
        [lazy_fixture("ot2_remote_everything_commit_id"), False],
        [lazy_fixture("ot2_local_source"), True],
    ],
)
def test_ot2_mounts(
    config: Dict[str, Any],
    monorepo_is_local: bool,
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts are created correctly when creating an OT-2."""
    config_file = convert_from_obj(config, testing_global_em_config, False)
    robot = config_file.robot_server
    emulator_proxy = config_file.emulator_proxy
    smoothie = config_file.smoothie_emulator
    monorepo_builder = config_file.monorepo_builder

    assert robot is not None
    check_correct_number_of_volumes(robot, 2)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", robot)
    assert partial_string_in_mount("monorepo-wheels:/dist", robot)

    assert emulator_proxy is not None
    check_correct_number_of_volumes(emulator_proxy, 2)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", emulator_proxy)
    assert partial_string_in_mount("monorepo-wheels:/dist", emulator_proxy)

    assert smoothie is not None
    check_correct_number_of_volumes(smoothie, 2)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", smoothie)
    assert partial_string_in_mount("monorepo-wheels:/dist", smoothie)

    assert monorepo_builder is not None
    check_correct_number_of_volumes(monorepo_builder, 2 if monorepo_is_local else 1)
    assert partial_string_in_mount("monorepo-wheels:/dist", monorepo_builder)

    if monorepo_is_local:
        assert partial_string_in_mount("/opentrons:/opentrons", monorepo_builder)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("thermocycler_module_firmware_remote"),
        lazy_fixture("thermocycler_module_firmware_local"),
        lazy_fixture("temperature_module_firmware_local"),
        lazy_fixture("temperature_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_local"),
        lazy_fixture("heater_shaker_module_firmware_local"),
        lazy_fixture("heater_shaker_module_firmware_remote"),
    ],
)
def test_module_monorepo_mounts(
    config: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts are created correctly when creating modules that use monorepo."""
    config_file = convert_from_obj(config, testing_global_em_config, False)
    modules = config_file.module_emulators
    monorepo_builder = config_file.monorepo_builder

    assert modules is not None
    assert monorepo_builder is not None
    assert len(modules) == 1

    module = modules[0]
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", module)
    assert partial_string_in_mount("monorepo-wheels:/dist", module)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("thermocycler_module_hardware_remote"),
        lazy_fixture("thermocycler_module_hardware_local"),
        lazy_fixture("heater_shaker_module_hardware_local"),
        lazy_fixture("heater_shaker_module_hardware_remote"),
    ],
)
def test_module_opentrons_modules_mounts(
    config: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test mounts are created correctly when creating modules that use opentrons-modules."""
    config_file = convert_from_obj(config, testing_global_em_config, False)
    modules = config_file.module_emulators
    opentrons_modules_builder = config_file.opentrons_modules_builder

    assert modules is not None
    assert opentrons_modules_builder is not None
    assert len(modules) == 1

    module = modules[0]
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", module)

    assert module.image is not None
    module_type = module.image.replace("-hardware", "")
    assert partial_string_in_mount(f"{module_type}-executable:/executable", module)


@pytest.mark.parametrize(
    "config_dict",
    [
        lazy_fixture("ot2_only"),
        lazy_fixture("ot3_only"),
        lazy_fixture("ot2_remote_everything_commit_id"),
        lazy_fixture("ot3_remote_everything_commit_id"),
        lazy_fixture("heater_shaker_module_hardware_remote"),
        lazy_fixture("heater_shaker_module_firmware_remote"),
        lazy_fixture("thermocycler_module_hardware_remote"),
        lazy_fixture("thermocycler_module_firmware_remote"),
        lazy_fixture("temperature_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_remote"),
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
        lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"),
        lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"),
        lazy_fixture("ot3_local_everything"),
        lazy_fixture("ot2_local_source"),
        lazy_fixture("heater_shaker_module_hardware_local"),
        lazy_fixture("heater_shaker_module_firmware_local"),
        lazy_fixture("thermocycler_module_hardware_local"),
        lazy_fixture("thermocycler_module_firmware_local"),
        lazy_fixture("temperature_module_firmware_local"),
        lazy_fixture("magnetic_module_firmware_local"),
    ],
)
def test_is_not_remote(
    config_dict: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm that when all source-types are not remote, is_remote is False."""
    config_file = convert_from_obj(config_dict, testing_global_em_config, False)
    assert not config_file.is_remote
