"""Parent class of all Robots. Subclass of HardwareModel.

Used to group all robots together and distinguish them from modules.
"""
import os.path
import pathlib
from typing import Any, Dict, List

from pydantic import Field, validator

from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    ROBOT_SERVER_MOUNT_NAME,
    DirectoryMount,
    MountTypes,
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import get_image_name


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

    def get_robot_server_mount_strings(self) -> List[str]:
        """Get mount string for a robot server, if source-type is local."""
        service_mount_path = os.path.basename(
            os.path.normpath(self.robot_server_source_location)
        )
        return (
            [
                DirectoryMount(
                    name=ROBOT_SERVER_MOUNT_NAME,
                    type=MountTypes.DIRECTORY,
                    source_path=pathlib.Path(self.robot_server_source_location),
                    mount_path=f"/{service_mount_path}",
                ).get_bind_mount_string()
            ]
            if self.robot_server_source_type == SourceType.LOCAL
            else []
        )

    def get_port_binding_string(self) -> str:
        """Get port binding string for Docker Compose file."""
        return f"{self.exposed_port}:{self.bound_port}"

    def get_image_name(self) -> str:
        """Get image name to run based off of passed parameters."""
        return get_image_name(
            self.hardware, self.robot_server_source_type, self.emulation_level
        )

    def get_source_repo(self) -> OpentronsRepository:
        """Override get_source_repo for robot-server."""
        return OpentronsRepository.OPENTRONS

    @property
    def is_remote(self) -> bool:
        """Check if all source-types are remote."""
        return super().is_remote and self.robot_server_source_type == SourceType.REMOTE
