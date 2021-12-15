"""Model and attributes for heater-shaker Module."""

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    HardwareDefinition,
    HeaterShakerModes,
)
from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    ModuleModel,
)


class HeaterShakerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Heater Shaker Module."""

    mode: HeaterShakerModes = HeaterShakerModes.SOCKET


class HeaterShakerModuleModel(ModuleModel):
    """Model for Heater Shaker Module."""

    hardware: Literal[HardwareDefinition.HEATER_SHAKER.id]
    hardware_specific_attributes: HeaterShakerModuleAttributes = Field(
        alias="hardware-specific-attributes", default=HeaterShakerModuleAttributes()
    )
