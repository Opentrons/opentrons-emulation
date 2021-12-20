"""Model and attributes for Magnetic Module."""
from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
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


class MagneticModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Magnetic Module."""

    pass


class MagneticModuleImages(Images):
    """Image names for Magnetic Module."""

    local_firmware_image_name: str = "magdeck-firmware-local"
    local_hardware_image_name: Literal[None] = None
    remote_firmware_image_name: str = "magdeck-firmware-remote"
    remote_hardware_image_name: Literal[None] = None


class MagneticModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: Literal[None] = None


class MagneticModuleInputModel(ModuleInputModel):
    """Model for Magnetic Module."""

    hardware: Literal[Hardware.MAGNETIC_MODULE]
    images: MagneticModuleImages = Field(default=MagneticModuleImages(), const=True)
    source_repos: MagneticModuleSourceRepositories = Field(
        default=MagneticModuleSourceRepositories(), const=True
    )
    hardware_specific_attributes: MagneticModuleAttributes = Field(
        alias="hardware-specific-attributes", default=MagneticModuleAttributes()
    )
    emulation_level: Literal[EmulationLevels.FIRMWARE] = Field(alias="emulation-level")
