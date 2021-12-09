from emulation_system.compose_file_creator.input.settings import (
    TemperatureModelSettings
)
from emulation_system.compose_file_creator.input.models.container_types.base_type import HardwareSpecificAttributes


class TemperatureModuleAttributes(HardwareSpecificAttributes):
    temperature: TemperatureModelSettings = TemperatureModelSettings()