"""Parent class of all Robots. Subclass of HardwareModel.

Used to group all robots together and distinguish them from modules.
"""
import os.path
import pathlib
from typing import Any, Dict, List

from pydantic import Field, validator

from emulation_system.compose_file_creator.config_file_settings import (
    DirectoryMount,
    MountTypes,
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.images import get_image_name
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateEnvironmentVariables,
)

from ..hardware_model import HardwareModel


class RobotInputModel(HardwareModel):
    """Parent class of all Robots. Subclass of HardwareModel.

    Used to group all robots together and distinguish them from modules.
    """

    exposed_port: int = Field(..., alias="exposed-port")
    bound_port: int

    robot_server_env_vars: IntermediateEnvironmentVariables | None = Field(
        alias="robot-server-env-vars"
    )
    emulator_proxy_env_vars: IntermediateEnvironmentVariables | None = Field(
        alias="emulator-proxy-env-vars"
    )

    def get_port_binding_string(self) -> str:
        """Get port binding string for Docker Compose file."""
        return f"{self.exposed_port}:{self.bound_port}"

    def get_image_name(self) -> str:
        """Get image name to run based off of passed parameters."""
        return get_image_name(
            self.hardware, self.robot_server_source_type, self.emulation_level
        )

    @property
    def is_remote(self) -> bool:
        """Check if all source-types are remote."""
        return super().is_remote and self.robot_server_source_type == SourceType.REMOTE
