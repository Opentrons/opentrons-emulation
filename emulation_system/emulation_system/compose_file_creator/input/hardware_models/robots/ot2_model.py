"""OT-2 Module and it's attributes."""
from pydantic.typing import NoneType
from typing_extensions import Literal

from pydantic import Field
from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.robots.robot_model import (  # noqa: E501
    RobotModel,
)

from emulation_system.compose_file_creator.config_file_settings import (
    Images,
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


class OT2Images(Images):
    """Image names for Magnetic Module."""
    local_firmware_image_name: str = "robot-server-local"
    local_hardware_image_name: NoneType = None
    remote_firmware_image_name: str = "robot-server-remote"
    remote_hardware_image_name: NoneType = None


class OT2SourceRepositories(SourceRepositories):
    """Source repositories for OT2."""
    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: NoneType = None


class OT2Model(RobotModel):
    """Model for OT2."""

    hardware: Literal["ot2"]
    images: OT2Images = Field(default=OT2Images(), const=True)
    source_repos: OT2SourceRepositories = Field(
        default=OT2SourceRepositories(), const=True
    )
    hardware_specific_attributes: OT2Attributes = Field(
        alias="hardware-specific-attributes", default=OT2Attributes()
    )
