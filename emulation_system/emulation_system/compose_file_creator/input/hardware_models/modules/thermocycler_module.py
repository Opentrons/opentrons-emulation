"""Model and attributes for Thermocycler Module."""
from typing_extensions import Literal

from pydantic import Field
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


class ThermocyclerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Thermocycler module."""

    lid_temperature: TemperatureModelSettings = Field(
        alias="lid-temperature", default=TemperatureModelSettings()
    )
    plate_temperature: TemperatureModelSettings = Field(
        alias="plate-temperature", default=TemperatureModelSettings()
    )


class ThermocyclerModuleModel(ModuleModel):
    """Model for Thermocycler Module."""

    hardware: Literal[HardwareDefinition.THERMOCYCLER.id]
    hardware_specific_attributes: ThermocyclerModuleAttributes = Field(
        alias="hardware-specific-attributes", default=ThermocyclerModuleAttributes()
    )
