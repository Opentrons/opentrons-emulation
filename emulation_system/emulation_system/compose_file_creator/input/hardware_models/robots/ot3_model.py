"""OT-3 Module and it's attributes."""
from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    PipetteSettings,
    SourceRepositories,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateEnvironmentVariables,
    IntermediatePorts,
)
from emulation_system.consts import OT3_STATE_MANAGER_BOUND_PORT

from ..hardware_specific_attributes import HardwareSpecificAttributes

# cannot import from . because of circular import issue
from .robot_model import RobotInputModel


class OT3Attributes(HardwareSpecificAttributes):
    """Attributes specific to OT3."""

    left: PipetteSettings = Field(default=PipetteSettings())
    right: PipetteSettings = Field(default=PipetteSettings())


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
    hardware_specific_attributes: OT3Attributes = Field(default=OT3Attributes())
    emulation_level: Literal[EmulationLevels.HARDWARE]
    bound_port: int = Field(default=31950)
    can_server_exposed_port: Optional[int]
    can_server_bound_port: int = Field(default=9898)
    ot3_state_manager_exposed_port: int = Field(default=OT3_STATE_MANAGER_BOUND_PORT)

    can_server_env_vars: IntermediateEnvironmentVariables | None
    gripper_env_vars: IntermediateEnvironmentVariables | None
    gantry_x_env_vars: IntermediateEnvironmentVariables | None
    gantry_y_env_vars: IntermediateEnvironmentVariables | None
    pipettes_env_vars: IntermediateEnvironmentVariables | None
    head_env_vars: IntermediateEnvironmentVariables | None
    bootloader_env_vars: IntermediateEnvironmentVariables | None
    state_manager_env_vars: IntermediateEnvironmentVariables | None

    def get_can_server_bound_port(self) -> Optional[IntermediatePorts]:
        """Get can server port string."""
        return (
            [f"{self.can_server_exposed_port}:{self.can_server_bound_port}"]
            if self.can_server_exposed_port is not None
            else None
        )

    def get_ot3_state_manager_bound_port(self) -> IntermediatePorts:
        """Get OT-3 State Manager bound port.

        Note that it is UDP protocol.
        """
        return [
            f"{self.ot3_state_manager_exposed_port}:{OT3_STATE_MANAGER_BOUND_PORT}/udp"
        ]
