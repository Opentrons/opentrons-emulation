"""Parent class of all Robots. Subclass of HardwareModel.

Used to group all robots together and distinguish them from modules.
"""
import os.path
import pathlib
from typing import (
    Any,
    Dict,
)

from pydantic import (
    Field,
    validator,
)

from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DirectoryMount,
    MountTypes,
    ROBOT_SERVER_MOUNT_NAME,
    SourceType,
)


class RobotInputModel(HardwareModel):
    """Parent class of all Robots. Subclass of HardwareModel.

    Used to group all robots together and distinguish them from modules.
    """

    exposed_port: int = Field(..., alias="exposed-port")
    bound_port: int
    robot_server_source_type: SourceType = Field(alias="robot-server-source-type")
    robot_server_source_location: str = Field(alias="robot-server-source-location")

    @validator("robot_server_source_location")
    def robot_server_check_source_location(cls, v: str, values: Dict[str, Any]) -> str:
        """If source type is local, confirms directory path specified exists."""
        return cls.validate_source_location("robot_server_source_type", v, values)

    def add_source_bind_mount(self) -> None:
        """If running a local type image add the mount to the mounts attribute."""
        super().add_source_bind_mount()
        service_mount_path = os.path.basename(
            os.path.normpath(self.robot_server_source_location)
        )
        if self.robot_server_source_type == SourceType.LOCAL:
            robot_server_mount = DirectoryMount(
                name=ROBOT_SERVER_MOUNT_NAME,
                type=MountTypes.DIRECTORY,
                source_path=pathlib.Path(self.robot_server_source_location),
                mount_path=f"/{service_mount_path}",
            )
            if robot_server_mount not in self.mounts:
                self.mounts.append(robot_server_mount)

    def get_port_binding_string(self) -> str:
        """Get port binding string for Docker Compose file."""
        return f"{self.exposed_port}:{self.bound_port}"
