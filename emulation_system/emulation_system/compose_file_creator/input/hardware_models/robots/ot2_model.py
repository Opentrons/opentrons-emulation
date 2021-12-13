from typing_extensions import Literal

from pydantic import Field
from emulation_system.compose_file_creator.input.hardware_models\
    .hardware_specific_attributes import HardwareSpecificAttributes
from emulation_system.compose_file_creator.input.hardware_models\
    .robots.robot_model import RobotModel

from emulation_system.compose_file_creator.input.settings import (
    PipetteSettings
)


class OT2Attributes(HardwareSpecificAttributes):
    left_pipette: PipetteSettings = Field(
        alias="left-pipette", default=PipetteSettings()
    )
    right_pipette: PipetteSettings = Field(
        alias="right-pipette", default=PipetteSettings()
    )


class OT2Model(RobotModel):
    hardware: Literal["OT-2"]
    hardware_specific_attributes: OT2Attributes = Field(
        alias="hardware-specific-attributes",
        default=OT2Attributes()
    )