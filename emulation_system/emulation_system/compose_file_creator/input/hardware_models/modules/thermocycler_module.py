from typing_extensions import Literal

from pydantic import Field
from compose_file_creator.settings import (
    TemperatureModelSettings, Hardware
)

from emulation_system.compose_file_creator.input.hardware_models\
    .hardware_specific_attributes import HardwareSpecificAttributes
from emulation_system.compose_file_creator.input.hardware_models\
    .modules.module_model import ModuleModel


class ThermocyclerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Thermocycler module"""
    lid_temperature: TemperatureModelSettings = Field(
        alias="lid-temperature", default=TemperatureModelSettings()
    )
    plate_temperature: TemperatureModelSettings = Field(
        alias="plate-temperature", default=TemperatureModelSettings()
    )


class ThermocyclerModuleModel(ModuleModel):
    """Model for Thermocycler Module"""
    hardware: Literal[Hardware.THERMOCYCLER.value]
    hardware_specific_attributes: ThermocyclerModuleAttributes = Field(
        alias="hardware-specific-attributes",
        default=ThermocyclerModuleAttributes()
    )