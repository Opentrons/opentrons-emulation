from pydantic import Field
from emulation_system.compose_file_creator.input.models.hardware_specific_attributes.base_type import HardwareSpecificAttributes
from emulation_system.compose_file_creator.input.settings import (
    TemperatureModelSettings
)

class ThermocyclerModuleAttributes(HardwareSpecificAttributes):
    lid_temperature: TemperatureModelSettings = Field(
        alias="lid-temperature", default=TemperatureModelSettings()
    )
    plate_temperature: TemperatureModelSettings = Field(
        alias="plate-temperature", default=TemperatureModelSettings()
    )
