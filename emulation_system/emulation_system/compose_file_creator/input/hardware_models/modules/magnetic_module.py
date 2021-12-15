"""Model and attributes for Magnetic Module."""
from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import HardwareDefinition
from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    ModuleModel,
)


class MagneticModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Magnetic Module."""

    pass


class MagneticModuleModel(ModuleModel):
    """Model for Magnetic Module."""

    hardware: Literal[HardwareDefinition.MAGNETIC.id]
    hardware_specific_attributes: MagneticModuleAttributes = Field(
        alias="hardware-specific-attributes", default=MagneticModuleAttributes()
    )
