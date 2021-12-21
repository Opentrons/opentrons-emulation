"""Model and attributes for heater-shaker Module."""

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    HeaterShakerModes,
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


class HeaterShakerModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: Literal[None] = None
    hardware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS_MODULES


class HeaterShakerModuleInputModel(ModuleInputModel):
    """Model for Heater Shaker Module."""

    hardware: Literal[Hardware.HEATER_SHAKER_MODULE]
    source_repos: HeaterShakerModuleSourceRepositories = Field(
        default=HeaterShakerModuleSourceRepositories(), const=True
    )
    hardware_specific_attributes: HeaterShakerModuleAttributes = Field(
        alias="hardware-specific-attributes", default=HeaterShakerModuleAttributes()
    )
    emulation_level: Literal[EmulationLevels.HARDWARE] = Field(alias="emulation-level")
