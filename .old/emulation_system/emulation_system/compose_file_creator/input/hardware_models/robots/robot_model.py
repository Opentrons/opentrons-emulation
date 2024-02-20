"""Parent class of all Robots. Subclass of HardwareModel.

Used to group all robots together and distinguish them from modules.
"""

import abc
from typing import TypeGuard

from pydantic import Field

from emulation_system.compose_file_creator.images import get_image_name
from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateEnvironmentVariables,
)

from ..hardware_model import HardwareModel


class RobotAttributes(HardwareSpecificAttributes, abc.ABC):
    """Attributes specific to Robots."""

    left_pipette: str | None
    right_pipette: str | None


class RobotInputModel(HardwareModel):
    """Parent class of all Robots. Subclass of HardwareModel.

    Used to group all robots together and distinguish them from modules.
    """

    exposed_port: int = Field(default=31950)
    bound_port: int = Field(default=31950)

    robot_server_env_vars: IntermediateEnvironmentVariables | None
    emulator_proxy_env_vars: IntermediateEnvironmentVariables | None
    hardware_specific_attributes: RobotAttributes

    def get_port_binding_string(self) -> str:
        """Get port binding string for Docker Compose file."""
        return f"{self.exposed_port}:{self.bound_port}"

    def get_image_name(self) -> str:
        """Get image name to run based off of passed parameters."""
        return get_image_name(self.hardware, self.emulation_level)

    @staticmethod
    def _has_pipette(pipette: str | None) -> TypeGuard[str]:
        return pipette is not None

    def has_left_pipette(self) -> bool:
        """Return True if left pipette is not None."""
        return self._has_pipette(self.hardware_specific_attributes.left_pipette)

    def has_right_pipette(self) -> bool:
        """Return True if right pipette is not None."""
        return self.hardware_specific_attributes.right_pipette is not None

    @property
    def right_pipette(self) -> str | None:
        """Return right pipette."""
        return self.hardware_specific_attributes.right_pipette

    @property
    def left_pipette(self) -> str | None:
        """Return left pipette."""
        return self.hardware_specific_attributes.left_pipette
