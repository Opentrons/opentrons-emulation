"""Parent class of all Robots. Subclass of HardwareModel.

Used to group all robots together and distinguish them from modules.
"""
from pydantic import Field

from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import Hardware


class RobotInputModel(HardwareModel):
    """Parent class of all Robots. Subclass of HardwareModel.

    Used to group all robots together and distinguish them from modules.
    """

    exposed_port: int = Field(..., alias="exposed-port")
    bound_port: int

    def is_ot3(self) -> bool:
        """Check if robot is ot3 or not."""
        # TODO: move to OT3InputModel when it is created.
        return self.hardware == Hardware.OT3

    def is_robot(self) -> bool:
        """If hardware is robot."""
        return True

    def get_port_binding_string(self) -> str:
        """Get port binding string for Docker Compose file."""
        return f"{self.exposed_port}:{self.bound_port}"
