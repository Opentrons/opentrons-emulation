"""Parent class of all Robots. Subclass of HardwareModel.

Used to group all robots together and distinguish them from modules.
"""
from pydantic import Field

from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
)


class RobotModel(HardwareModel):
    """Parent class of all Robots. Subclass of HardwareModel.

    Used to group all robots together and distinguish them from modules.
    """

    exposed_port: int = Field(..., alias="exposed-port")
    bound_port: int

    def get_port_binding_string(self) -> str:
        """Get port binding string for Docker Compose file."""
        return f"{self.exposed_port}:{self.bound_port}"
