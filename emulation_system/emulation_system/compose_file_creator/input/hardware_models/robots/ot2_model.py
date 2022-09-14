"""OT-2 Module and it's attributes."""
from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    PipetteSettings,
    SourceRepositories,
)

from ..hardware_specific_attributes import HardwareSpecificAttributes

# cannot import from . because of circular import issue
from .robot_model import RobotInputModel


class OT2Attributes(HardwareSpecificAttributes):
    """Attributes specific to OT2."""

    left: PipetteSettings = Field(alias="left-pipette", default=PipetteSettings())
    right: PipetteSettings = Field(alias="right-pipette", default=PipetteSettings())


class OT2SourceRepositories(SourceRepositories):
    """Source repositories for OT2."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: Literal[None] = None


class OT2InputModel(RobotInputModel):
    """Model for OT2."""

    hardware: Literal[Hardware.OT2]
    source_repos: OT2SourceRepositories = Field(
        default=OT2SourceRepositories(), const=True, exclude=True
    )
    hardware_specific_attributes: OT2Attributes = Field(
        alias="hardware-specific-attributes", default=OT2Attributes()
    )
    emulation_level: Literal[EmulationLevels.FIRMWARE] = Field(alias="emulation-level")
    bound_port: int = Field(alias="bound-port", default=31950)
