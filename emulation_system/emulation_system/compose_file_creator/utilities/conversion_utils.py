from typing import Union

from emulation_system import SystemConfigurationModel
from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
)
from emulation_system.compose_file_creator.utilities.hardware_utils import (
    is_module,
    is_robot,
)
from emulation_system.source import MonorepoSource, OpentronsModulesSource


def is_hardware_level_module(container: HardwareModel) -> bool:
    return is_module(container) and container.is_hardware_emulation_level()


def is_firmware_level_module(container: HardwareModel) -> bool:
    return is_module(container) and container.is_firmware_emulation_level()


def get_input_container_source(
    container: HardwareModel, config_model: SystemConfigurationModel
) -> Union[MonorepoSource, OpentronsModulesSource]:
    source: Union[MonorepoSource, OpentronsModulesSource]

    if is_robot(container):
        source = config_model.monorepo_source
    elif is_firmware_level_module(container):
        source = config_model.monorepo_source
    elif is_hardware_level_module(container):
        source = config_model.opentrons_modules_source
    else:
        raise ValueError(
            f"Cannot determine source for {container.id} (Hardware Type: {container.hardware})"
        )

    return source
