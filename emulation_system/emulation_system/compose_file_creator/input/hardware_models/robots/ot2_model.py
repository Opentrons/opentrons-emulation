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
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateEnvironmentVariables,
)

from ..hardware_specific_attributes import HardwareSpecificAttributes

# cannot import from . because of circular import issue
from .robot_model import RobotInputModel


class OT2Attributes(HardwareSpecificAttributes):
    """Attributes specific to OT2."""

    left_pipette: PipetteSettings = Field(default=PipetteSettings())
    right_pipette: PipetteSettings = Field(default=PipetteSettings())


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
    hardware_specific_attributes: OT2Attributes = Field(default=OT2Attributes())
    emulation_level: Literal[EmulationLevels.FIRMWARE]
    bound_port: int = Field(default=31950)
    smoothie_env_vars: IntermediateEnvironmentVariables | None
