import os
from typing import (
    Callable,
)

import pytest
import yaml

from e2e.utilities.helper_functions import get_container
from e2e.utilities.ot3_system import OT3System
from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.consts import (
    ROOT_DIR,
)


@pytest.fixture
def model_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    def _model_under_test(relative_path: str) -> OT3System:
        abs_path = os.path.join(ROOT_DIR, relative_path)
        with open(abs_path, "r") as file:
            contents = yaml.safe_load(file)
        system: RuntimeComposeFileModel = convert_from_obj(
            contents, testing_global_em_config, False
        )

        return OT3System(
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
