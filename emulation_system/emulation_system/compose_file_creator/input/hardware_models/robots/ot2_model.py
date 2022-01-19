"""OT-2 Module and it's attributes."""
from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.robots.robot_model import (  # noqa: E501
    RobotModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    PipetteSettings,
    SourceRepositories,
)


class OT2Attributes(HardwareSpecificAttributes):
    """Attributes specific to OT2."""

    left_pipette: PipetteSettings = Field(
        alias="left-pipette", default=PipetteSettings()
    )
    right_pipette: PipetteSettings = Field(
        alias="right-pipette", default=PipetteSettings()
    )


class OT2SourceRepositories(SourceRepositories):
    """Source repositories for OT2."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: Literal[None] = None


class OT2InputModel(RobotModel):
    """Model for OT2."""

    hardware: Literal[Hardware.OT2]
    source_repos: OT2SourceRepositories = Field(
        default=OT2SourceRepositories(), const=True
    )
    hardware_specific_attributes: OT2Attributes = Field(
        alias="hardware-specific-attributes", default=OT2Attributes()
    )
    emulation_level: Literal[EmulationLevels.FIRMWARE] = Field(alias="emulation-level")
    bound_port: int = Field(alias="bound-port", default=31950)
