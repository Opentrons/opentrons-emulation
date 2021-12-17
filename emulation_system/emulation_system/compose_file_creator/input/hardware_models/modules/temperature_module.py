"""Model and attributes for Temperature Module."""
from pydantic import Field
from pydantic.typing import NoneType
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
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


class TemperatureModuleImages(Images):
    """Image names for Temperature Module."""
    local_firmware_image_name: str = "tempdeck-firmware-local"
    local_hardware_image_name: NoneType = None
    remote_firmware_image_name: str = "tempdeck-firmware-remote"
    remote_hardware_image_name: NoneType = None


class TemperatureModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Temperature Module."""

    temperature: TemperatureModelSettings = TemperatureModelSettings()


class TemperatureModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""
    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: NoneType = None


class TemperatureModuleInputModel(ModuleInputModel):
    """Model for Temperature Module."""

    hardware: Literal["temperature-module"]
    images: TemperatureModuleImages = Field(
        default=TemperatureModuleImages(), const=True
    )
    source_repos: TemperatureModuleSourceRepositories = Field(
        default=TemperatureModuleSourceRepositories(), const=True
    )
    hardware_specific_attributes: TemperatureModuleAttributes = Field(
        alias="hardware-specific-attributes", default=TemperatureModuleAttributes()
    )
