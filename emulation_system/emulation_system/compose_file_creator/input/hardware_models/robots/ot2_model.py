"""OT-2 Module and it's attributes."""
from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceRepositories,
)
from emulation_system.compose_file_creator.pipette_utils import get_valid_ot2_pipettes
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateEnvironmentVariables,
)

# cannot import from . because of circular import issue
from .robot_model import RobotAttributes, RobotInputModel


class OT2Attributes(RobotAttributes):
    """Attributes specific to Robots."""

    ####################################################
    # NOTE: Calling a method to define types is WERID. #
    #   Refer to pipette_utils.py for an explanation   #
    ####################################################

    left_pipette: get_valid_ot2_pipettes() | None = None  # type: ignore[valid-type]
    right_pipette: get_valid_ot2_pipettes() | None = None  # type: ignore[valid-type]


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
    smoothie_env_vars: IntermediateEnvironmentVariables | None
