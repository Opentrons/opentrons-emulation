"""OT-2 Module and it's attributes."""
from typing_extensions import Literal

from pydantic import Field
from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.robots.robot_model import (  # noqa: E501
    RobotModel,
)

from emulation_system.compose_file_creator.config_file_settings import (
    PipetteSettings,
    Hardware,
)


class OT2Attributes(HardwareSpecificAttributes):
    """Attributes specific to OT2."""

    left_pipette: PipetteSettings = Field(
        alias="left-pipette", default=PipetteSettings()
    )
    right_pipette: PipetteSettings = Field(
        alias="right-pipette", default=PipetteSettings()
    )


class OT2Model(RobotModel):
    """Model for OT2."""

    hardware: Literal[Hardware.OT2]
    hardware_specific_attributes: OT2Attributes = Field(
        alias="hardware-specific-attributes", default=OT2Attributes()
    )
