"""Model and attributes for Temperature Module."""
from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    TemperatureModelSettings,
    HardwareDefinition,
)
from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    ModuleModel,
)


class TemperatureModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Temperature Module."""

    temperature: TemperatureModelSettings = TemperatureModelSettings()


class TemperatureModuleModel(ModuleModel):
    """Model for Temperature Module."""

    hardware: Literal[HardwareDefinition.TEMPERATURE.id]
    hardware_specific_attributes: TemperatureModuleAttributes = Field(
        alias="hardware-specific-attributes", default=TemperatureModuleAttributes()
    )
