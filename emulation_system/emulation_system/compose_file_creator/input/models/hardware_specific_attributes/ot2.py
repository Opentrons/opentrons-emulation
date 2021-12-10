from pydantic import Field
from emulation_system.compose_file_creator.input.models.hardware_specific_attributes.base_type import HardwareSpecificAttributes
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
