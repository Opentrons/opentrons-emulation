from emulation_system.compose_file_creator.input.settings import (
    TemperatureModelSettings
)
from emulation_system.compose_file_creator.input.hardware_models\
    .hardware_specific_attributes import HardwareSpecificAttributes
from emulation_system.compose_file_creator.input.hardware_models\
    .modules.module_model import ModuleModel


class TemperatureModuleAttributes(HardwareSpecificAttributes):
    temperature: TemperatureModelSettings = TemperatureModelSettings()


class TemperatureModuleModel(ModuleModel):
    pass