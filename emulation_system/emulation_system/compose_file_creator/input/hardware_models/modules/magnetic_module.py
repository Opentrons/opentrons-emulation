from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.input.settings import Hardware
from emulation_system.compose_file_creator.input.hardware_models\
    .hardware_specific_attributes import HardwareSpecificAttributes
from emulation_system.compose_file_creator.input.hardware_models\
    .modules.module_model import ModuleModel


class MagneticModuleAttributes(HardwareSpecificAttributes):
    pass


class MagneticModuleModel(ModuleModel):
    hardware: Literal[Hardware.MAGNETEIC.value]
    hardware_specific_attributes: MagneticModuleAttributes = Field(
        alias="hardware-specific-attributes",
        default=MagneticModuleAttributes()
    )