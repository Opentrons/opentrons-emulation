"""Module for pipette utilities."""


from enum import Enum

from emulation_system.compose_file_creator.pipette_utils.data_models import (
    PipetteInfo,
    RobotPipettes,
)
from emulation_system.compose_file_creator.pipette_utils.lookups import (
    OT2PipetteLookup,
    OT3PipetteLookup,
    lookup_pipette,
)


def get_robot_pipettes(
    robot_type: str, left_pipette: str | None, right_pipette: str | None
) -> RobotPipettes:
    """Gets pipettes for robot."""
    left_pipette_info = (
        None
        if left_pipette is None
        else PipetteInfo.from_pipette_lookup(lookup_pipette(left_pipette, robot_type))
    )
    right_pipette_info = (
        None
        if not right_pipette is not None
        else PipetteInfo.from_pipette_lookup(lookup_pipette(right_pipette, robot_type))
    )

    return RobotPipettes(left=left_pipette_info, right=right_pipette_info)


def get_valid_ot2_pipettes() -> Enum:
    """Gets valid OT-2 pipettes."""
    return OT2PipetteLookup.get_valid_pipette_names()


def get_valid_ot3_pipettes() -> Enum:
    """Gets valid OT-3 pipettes."""
    return OT3PipetteLookup.get_valid_pipette_names()
