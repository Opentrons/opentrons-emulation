"""pytest conftest file for e2e testing"""
import os
from typing import Callable

import pytest
import yaml
from pydantic import parse_obj_as

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.consts import ROOT_DIR
from tests.e2e.consts import BindMountInfo
from tests.e2e.docker_interface.e2e_system import (
    DefaultContainers,
    E2EHostSystem,
    ExpectedBindMounts,
)
from tests.e2e.docker_interface.module_containers import ModuleContainers
from tests.e2e.docker_interface.ot3_containers import OT3SystemUnderTest
from tests.e2e.helper_functions import get_container, get_containers


@pytest.fixture
def ot3_model_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable[[str], OT3SystemUnderTest]:
    """Pytest fixture to generate OT3SystemUnderTest object based of a path to a yaml configuration file.

    This method will actually create a Callable object that when called is the OT3SystemUnderTest object.
    """

    def _model_under_test(relative_path: str) -> OT3SystemUnderTest:
        abs_path = os.path.join(ROOT_DIR, relative_path)
        with open(abs_path, "r") as file:
            contents = yaml.safe_load(file)
        system: RuntimeComposeFileModel = convert_from_obj(
            contents, testing_global_em_config, False
        )

        return OT3SystemUnderTest(
            gantry_x=get_container(system.ot3_gantry_x_emulator),
            gantry_y=get_container(system.ot3_gantry_y_emulator),
            head=get_container(system.ot3_head_emulator),
            gripper=get_container(system.ot3_gripper_emulator),
            pipettes=get_container(system.ot3_pipette_emulator),
            bootloader=get_container(system.ot3_bootloader_emulator),
            state_manager=get_container(system.ot3_state_manager),
            can_server=get_container(system.can_server),
            firmware_builder=get_container(system.ot3_firmware_builder),
        )

    return _model_under_test


@pytest.fixture
def modules_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable[[str], ModuleContainers]:
    """Pytest fixture to generate ModuleContainerNames object based of a path to a yaml configuration file.

    This method will actually create a Callable object that when called is the ModuleContainerNames object.
    """

    def _model_under_test(relative_path: str) -> ModuleContainers:
        abs_path = os.path.join(ROOT_DIR, relative_path)
        with open(abs_path, "r") as file:
            contents = yaml.safe_load(file)
        system: RuntimeComposeFileModel = convert_from_obj(
            contents, testing_global_em_config, False
        )

        return ModuleContainers(
            hardware_emulation_thermocycler_modules=get_containers(
                system.hardware_level_thermocycler_module_emulators
            ),
            firmware_emulation_thermocycler_modules=get_containers(
                system.firmware_level_thermocycler_module_emulators
            ),
            hardware_emulation_heater_shaker_modules=get_containers(
                system.hardware_level_heater_shaker_module_emulators
            ),
            firmware_emulation_heater_shaker_modules=get_containers(
                system.firmware_level_heater_shaker_module_emulators
            ),
            firmware_emulation_magnetic_modules=get_containers(
                system.magnetic_module_emulators
            ),
            firmware_emulation_temperature_modules=get_containers(
                system.temperature_module_emulators
            ),
            emulator_proxy=get_container(system.emulator_proxy),
            opentrons_modules_builder=get_container(system.opentrons_modules_builder),
        )

    return _model_under_test


@pytest.fixture
def default_containers_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable[[str], DefaultContainers]:
    """Pytest fixture to generate ModuleContainerNames object based of a path to a yaml configuration file.

    This method will actually create a Callable object that when called is the ModuleContainerNames object.
    """

    def _model_under_test(relative_path: str) -> DefaultContainers:
        abs_path = os.path.join(ROOT_DIR, relative_path)
        with open(abs_path, "r") as file:
            contents = yaml.safe_load(file)
        system: RuntimeComposeFileModel = convert_from_obj(
            contents, testing_global_em_config, False
        )

        return DefaultContainers(
            robot_server=get_container(system.robot_server),
            monorepo_builder=get_container(system.monorepo_builder),
        )

    return _model_under_test


@pytest.fixture
def local_mounts_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable[[str], ExpectedBindMounts]:
    """Pytest fixture to generate ExpectedBindMount object based of a path to a yaml configuration file.

    This method will actually create a Callable object that when called is the ExpectedBindMount object.
    """

    def _model_under_test(relative_path: str) -> ExpectedBindMounts:
        abs_path = os.path.join(ROOT_DIR, relative_path)
        with open(abs_path, "r") as file:
            contents = yaml.safe_load(file)

        model = parse_obj_as(SystemConfigurationModel, contents)
        monorepo_bind_mount = (
            None
            if model.monorepo_source.is_remote()
            else BindMountInfo(model.monorepo_source.source_location, "/opentrons")
        )
        firmware_bind_mount = (
            None
            if model.ot3_firmware_source.is_remote()
            else BindMountInfo(
                model.ot3_firmware_source.source_location, "/ot3-firmware"
            )
        )
        modules_bind_mount = (
            None
            if model.opentrons_modules_source.is_remote()
            else BindMountInfo(
                model.opentrons_modules_source.source_location, "/opentrons-modules"
            )
        )
        return ExpectedBindMounts(
            MONOREPO=monorepo_bind_mount,
            FIRMWARE=firmware_bind_mount,
            MODULES=modules_bind_mount,
        )

    return _model_under_test


@pytest.fixture
def e2e_host(
    testing_global_em_config: OpentronsEmulationConfiguration,
    ot3_model_under_test: Callable[[str], OT3SystemUnderTest],
    modules_under_test: Callable[[str], ModuleContainers],
    local_mounts_under_test: Callable[[str], ExpectedBindMounts],
    default_containers_under_test: Callable[[str], DefaultContainers],
) -> Callable[[str], E2EHostSystem]:
    """Load top-level e2e system from docker."""

    def _model_under_test(relative_path: str) -> E2EHostSystem:
        return E2EHostSystem(
            ot3_containers=ot3_model_under_test(relative_path),
            module_containers=modules_under_test(relative_path),
            expected_binds_mounts=local_mounts_under_test(relative_path),
            default_containers=default_containers_under_test(relative_path),
        )

    return _model_under_test
