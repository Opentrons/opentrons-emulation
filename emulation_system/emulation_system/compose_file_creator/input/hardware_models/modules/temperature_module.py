from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.input.settings import (
    TemperatureModelSettings, Hardware
)
from emulation_system.compose_file_creator.input.hardware_models\
    .hardware_specific_attributes import HardwareSpecificAttributes
from emulation_system.compose_file_creator.input.hardware_models\
    .modules.module_model import ModuleModel


class TemperatureModuleAttributes(HardwareSpecificAttributes):
    temperature: TemperatureModelSettings = TemperatureModelSettings()


class TemperatureModuleModel(ModuleModel):
    hardware: Literal[Hardware.TEMPERATURE.value]
    hardware_specific_attributes: TemperatureModuleAttributes = Field(
        alias="hardware-specific-attributes",
        default=TemperatureModuleAttributes()
    )