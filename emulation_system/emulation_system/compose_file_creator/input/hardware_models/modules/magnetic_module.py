"""Model and attributes for Magnetic Module."""
from pydantic import Field
from pydantic.typing import NoneType
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
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
    local_hardware_image_name: NoneType = None
    remote_firmware_image_name: str = "magdeck-firmware-remote"
    remote_hardware_image_name: NoneType = None


class MagneticModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""
    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: NoneType = None


class MagneticModuleInputModel(ModuleInputModel):
    """Model for Magnetic Module."""

    hardware: Literal["magnetic-module"]
    images: MagneticModuleImages = Field(default=MagneticModuleImages(), const=True)
    source_repos: MagneticModuleSourceRepositories = Field(
        default=MagneticModuleSourceRepositories(), const=True
    )
    hardware_specific_attributes: MagneticModuleAttributes = Field(
        alias="hardware-specific-attributes", default=MagneticModuleAttributes()
    )
