"""OT-3 Module and it's attributes."""
import os
import pathlib
from typing import (
    List,
    Optional,
    Union,
    cast,
)

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.robots.robot_model import (  # noqa: E501
    RobotInputModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import Port
from emulation_system.compose_file_creator.settings.config_file_settings import (
    CAN_SERVER_MOUNT_NAME,
    DirectoryMount,
    EmulationLevels,
    Hardware,
    MountTypes,
    OpentronsRepository,
    PipetteSettings,
    SourceRepositories,
    SourceType,
)


class OT3Attributes(HardwareSpecificAttributes):
    """Attributes specific to OT3."""

    left: PipetteSettings = Field(alias="left-pipette", default=PipetteSettings())
    right: PipetteSettings = Field(alias="right-pipette", default=PipetteSettings())


class OT3SourceRepositories(SourceRepositories):
    """Source repositories for OT3."""

    firmware_repo_name: Literal[None] = None
    # This is the monorepo because we are specifying where the robot server
    # should get it's source code. Not the hardware emulators, those are hardcoded
    # to ot3-firmware
    hardware_repo_name: OpentronsRepository = OpentronsRepository.OT3_FIRMWARE


class OT3InputModel(RobotInputModel):
    """Model for OT3."""

    hardware: Literal[Hardware.OT3]
    source_repos: OT3SourceRepositories = Field(
        default=OT3SourceRepositories(), const=True, exclude=True
    )
    can_server_source_type: SourceType = Field(alias="can-server-source-type")
    can_server_source_location: str = Field(alias="can-server-source-location")

    hardware_specific_attributes: OT3Attributes = Field(
        alias="hardware-specific-attributes", default=OT3Attributes()
    )
    emulation_level: Literal[EmulationLevels.HARDWARE] = Field(alias="emulation-level")
    bound_port: int = Field(alias="bound-port", default=31950)
    can_server_exposed_port: Optional[int] = Field(alias="can-server-exposed-port")
    can_server_bound_port: int = Field(alias="can-server-bound-port", default=9898)

    def get_can_mount_strings(self) -> List[str]:
        """Get mount strings for can service."""
        service_mount_path = os.path.basename(
            os.path.normpath(self.can_server_source_location)
        )
        return (
            [
                DirectoryMount(
                    name=CAN_SERVER_MOUNT_NAME,
                    type=MountTypes.DIRECTORY,
                    source_path=pathlib.Path(self.can_server_source_location),
                    mount_path=f"/{service_mount_path}",
                ).get_bind_mount_string()
            ]
            if self.can_server_source_type == SourceType.LOCAL
            else []
        )

    def get_can_server_bound_port(self) -> Optional[List[Union[float, str, Port]]]:
        """Get can server port string."""
        return (
            cast(
                 List[Union[float, str, Port]],
                 [f"{self.can_server_exposed_port}:{self.can_server_bound_port}"]
            )
            if self.can_server_exposed_port is not None
            else None
        )

    @property
    def is_remote(self) -> bool:
        """Check if all source-types are remote."""
        return super().is_remote and self.can_server_source_type == SourceType.REMOTE
