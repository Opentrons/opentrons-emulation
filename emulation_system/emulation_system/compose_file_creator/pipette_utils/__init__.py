"""Module for pipette utilities."""


from emulation_system.compose_file_creator.pipette_utils.data_models import (
    PipetteInfo,
    RobotPipettes,
)
from emulation_system.compose_file_creator.pipette_utils.lookups import lookup_pipette


def get_robot_pipettes(
    robot_type: str, left_pipette: str | None, right_pipette: str | None
) -> RobotPipettes:
    """Gets pipettes for robot."""
    left_pipette_info = (
        None
        if left_pipette is None
        else PipetteInfo(lookup_pipette(left_pipette, robot_type))
    )
    right_pipette_info = (
        None
        if not right_pipette is not None
        else PipetteInfo(lookup_pipette(right_pipette, robot_type))
    )

    return RobotPipettes(left=left_pipette_info, right=right_pipette_info)
