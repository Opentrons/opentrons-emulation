"""Module for pipette utilities."""


from emulation_system.compose_file_creator.input.hardware_models.robots import (
    robot_model,
)
from emulation_system.compose_file_creator.pipette_utils.data_models import (
    PipetteInfo,
    RobotPipettes,
)
from emulation_system.compose_file_creator.pipette_utils.lookups import lookup_pipette


def get_robot_pipettes(robot: robot_model.RobotInputModel) -> RobotPipettes:
    """Gets pipettes for robot."""
    hw = robot.hardware

    left_pipette: PipetteInfo | None = (
        None
        if robot.left_pipette is None
        else PipetteInfo.from_pipette_lookup_value(
            lookup_pipette(robot.left_pipette, hw)
        )
    )
    right_pipette: PipetteInfo | None = (
        None
        if not robot.right_pipette is not None
        else PipetteInfo.from_pipette_lookup_value(
            lookup_pipette(robot.right_pipette, hw)
        )
    )

    return RobotPipettes(left=left_pipette, right=right_pipette)
