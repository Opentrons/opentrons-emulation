"""Model and attributes for Magnetic Module."""
from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
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


class MagneticModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: Literal[None] = None


class MagneticModuleInputModel(ModuleInputModel):
    """Model for Magnetic Module."""

    hardware: Literal[Hardware.MAGNETIC_MODULE]
    source_repos: MagneticModuleSourceRepositories = Field(
        default=MagneticModuleSourceRepositories(), const=True
    )
    hardware_specific_attributes: MagneticModuleAttributes = Field(
        alias="hardware-specific-attributes", default=MagneticModuleAttributes()
    )
    emulation_level: Literal[EmulationLevels.FIRMWARE] = Field(alias="emulation-level")

    def is_magnetic_module(self) -> bool:
        """If hardware is a Magnetic Module."""
        return True
