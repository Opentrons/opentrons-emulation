"""Module for pipette utilities."""

from typing import Type, Union

from emulation_system.compose_file_creator.input.hardware_models.robots import (
    robot_model,
)
from emulation_system.compose_file_creator.pipette_utils.data_models import (
    PipetteInfo,
    RobotPipettes,
)
from emulation_system.compose_file_creator.pipette_utils.lookups import (
    OT2PipetteLookup,
    OT3PipetteLookup,
)


def _get_pipette_by_name(
    name: str, pipette_lookup: Union[Type[OT2PipetteLookup], Type[OT3PipetteLookup]]
) -> "PipetteInfo":
    """Looks up enum by name."""
    for _, pipette_def in pipette_lookup.__members__.items():
        if name in [pipette_def.pipette_name, pipette_def.display_name]:
            return PipetteInfo.from_pipette_lookup_value(pipette_def)
    raise ValueError(f"Pipette with name {name} not found.")


def get_robot_pipettes(robot: robot_model.RobotInputModel) -> RobotPipettes:
    """Gets pipettes for robot."""
    left_pipette: PipetteInfo | None
    right_pipette: PipetteInfo | None
    pipette_lookup: Union[Type[OT2PipetteLookup], Type[OT3PipetteLookup]] = (
        OT2PipetteLookup if robot.hardware == "ot2" else OT3PipetteLookup
    )

    left_pipette = (
        None
        if robot.left_pipette is None
        else _get_pipette_by_name(robot.left_pipette, pipette_lookup)
    )
    right_pipette = (
        None
        if not robot.right_pipette is not None
        else _get_pipette_by_name(robot.right_pipette, pipette_lookup)
    )

    return RobotPipettes(left=left_pipette, right=right_pipette)
