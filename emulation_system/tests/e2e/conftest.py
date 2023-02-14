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
from tests.e2e.utilities.consts import ExpectedMount
from tests.e2e.utilities.expected_bind_mounts import ExpectedBindMounts
from tests.e2e.utilities.helper_functions import get_container, get_containers
from tests.e2e.utilities.module_containers import ModuleContainers
from tests.e2e.utilities.ot3_containers import OT3Containers


@pytest.fixture
def ot3_model_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    """Pytest fixture to generate OT3Containers object based of a path to a yaml configuration file.

    This method will actually create a Callable object that when called is the OT3Containers object.
    """

    def _model_under_test(relative_path: str) -> OT3Containers:
        abs_path = os.path.join(ROOT_DIR, relative_path)
        with open(abs_path, "r") as file:
            contents = yaml.safe_load(file)
        system: RuntimeComposeFileModel = convert_from_obj(
            contents, testing_global_em_config, False
        )

        return OT3Containers(
            gantry_x=get_container(system.ot3_gantry_x_emulator),
            gantry_y=get_container(system.ot3_gantry_y_emulator),
            head=get_container(system.ot3_head_emulator),
            gripper=get_container(system.ot3_gripper_emulator),
            pipettes=get_container(system.ot3_pipette_emulator),
            bootloader=get_container(system.ot3_bootloader_emulator),
            state_manager=get_container(system.ot3_state_manager),
            robot_server=get_container(system.robot_server),
            can_server=get_container(system.can_server),
            emulator_proxy=get_container(system.emulator_proxy),
            firmware_builder=get_container(system.ot3_firmware_builder),
            monorepo_builder=get_container(system.monorepo_builder),
            modules_builder=get_container(system.opentrons_modules_builder),
        )

    return _model_under_test


@pytest.fixture
def modules_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    """Pytest fixture to generate ModuleContainers object based of a path to a yaml configuration file.

    This method will actually create a Callable object that when called is the ModuleContainers object.
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
        )

    return _model_under_test


@pytest.fixture
def local_mounts_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
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
            else ExpectedMount(model.monorepo_source.source_location, "/opentrons")
        )
        firmware_bind_mount = (
            None
            if model.ot3_firmware_source.is_remote()
            else ExpectedMount(
                model.ot3_firmware_source.source_location, "/ot3-firmware"
            )
        )
        modules_bind_mount = (
            None
            if model.opentrons_modules_source.is_remote()
            else ExpectedMount(
                model.opentrons_modules_source.source_location, "/opentrons-modules"
            )
        )
        return ExpectedBindMounts(
            MONOREPO=monorepo_bind_mount,
            FIRMWARE=firmware_bind_mount,
            MODULES=modules_bind_mount,
        )

    return _model_under_test
