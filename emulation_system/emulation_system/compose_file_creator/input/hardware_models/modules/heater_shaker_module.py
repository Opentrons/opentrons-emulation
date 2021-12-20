"""Model and attributes for heater-shaker Module."""

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    HeaterShakerModes,
    Images,
    OpentronsRepository,
    SourceRepositories,
)
from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    ModuleInputModel,
)


class HeaterShakerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Heater Shaker Module."""

    mode: HeaterShakerModes = HeaterShakerModes.SOCKET


class HeaterShakerModuleImages(Images):
    """Image names for Heater-Shaker."""
    local_firmware_image_name: Literal[None] = None
    local_hardware_image_name: str = "heater-shaker-hardware-local"
    remote_firmware_image_name: Literal[None] = None
    remote_hardware_image_name: str = "heater-shaker-hardware-remote"


class HeaterShakerModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""
    firmware_repo_name: Literal[None] = None
    hardware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS_MODULES


class HeaterShakerModuleInputModel(ModuleInputModel):
    """Model for Heater Shaker Module."""
    hardware: Literal[Hardware.HEATER_SHAKER_MODULE]
    images: HeaterShakerModuleImages = Field(
        default=HeaterShakerModuleImages(), const=True
    )
    source_repos: HeaterShakerModuleSourceRepositories = Field(
        default=HeaterShakerModuleSourceRepositories(), const=True
    )
    hardware_specific_attributes: HeaterShakerModuleAttributes = Field(
        alias="hardware-specific-attributes", default=HeaterShakerModuleAttributes()
    )
    emulation_level: Literal[EmulationLevels.HARDWARE] = Field(alias="emulation-level")
