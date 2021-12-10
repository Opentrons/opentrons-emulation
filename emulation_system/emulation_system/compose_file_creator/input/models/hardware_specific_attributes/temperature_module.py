from emulation_system.compose_file_creator.input.settings import (
    TemperatureModelSettings
)
from emulation_system.compose_file_creator.input.models.hardware_specific_attributes.base_type import HardwareSpecificAttributes


class TemperatureModuleAttributes(HardwareSpecificAttributes):
    temperature: TemperatureModelSettings = TemperatureModelSettings()