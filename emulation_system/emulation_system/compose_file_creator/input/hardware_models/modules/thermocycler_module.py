"""Model and attributes for Thermocycler Module."""
from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Images,
    OpentronsRepository,
    SourceRepositories,
    TemperatureModelSettings,
)
from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    ModuleInputModel,
)


class ThermocyclerModuleImages(Images):
    """Image names for Magnetic Module."""
    local_firmware_image_name: str = "thermocycler-firmware-local"
    local_hardware_image_name: str = "thermocycler-hardware-local"
    remote_firmware_image_name: str = "thermocycler-firmware-remote"
    remote_hardware_image_name: str = "thermocycler-hardware-remote"


class ThermocyclerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Thermocycler module."""

    lid_temperature: TemperatureModelSettings = Field(
        alias="lid-temperature", default=TemperatureModelSettings()
    )
    plate_temperature: TemperatureModelSettings = Field(
        alias="plate-temperature", default=TemperatureModelSettings()
    )


class ThermocyclerModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""
    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS_MODULES


class ThermocyclerModuleInputModel(ModuleInputModel):
    """Model for Thermocycler Module."""

    hardware: Literal["thermocycler-module"]
    images: ThermocyclerModuleImages = Field(
        default=ThermocyclerModuleImages(), const=True
    )
    source_repos: ThermocyclerModuleSourceRepositories = Field(
        default=ThermocyclerModuleSourceRepositories(), const=True
    )
    hardware_specific_attributes: ThermocyclerModuleAttributes = Field(
        alias="hardware-specific-attributes", default=ThermocyclerModuleAttributes()
    )
    emulation_level: Literal[
        EmulationLevels.FIRMWARE
    ] = Field(alias="emulation-level")
