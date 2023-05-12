"""Module containing helper class to access OT-3 Containers for local system"""

from dataclasses import dataclass
from typing import Optional

from docker.models.containers import Container  # type: ignore[import]

from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)
from tests.e2e.helper_functions import get_mounts
from tests.e2e.test_definition.build_arg_configurations import BuildArgConfigurations


@dataclass
class OT3SystemUnderTest:
    """Dataclass to access all containers in OT-3 System easily."""

    gantry_x: Container
    gantry_y: Container
    head: Container
    gripper: Container
    pipettes: Container
    bootloader: Container
    state_manager: Container
    can_server: Container

    firmware_builder: Optional[Container]

    @property
    def ot3_firmware_builder_created(self) -> bool:
        """Whether or not the ot3-firmware builder container was created."""
        return self.firmware_builder is not None

    @property
    def local_ot3_firmware_mounted(self) -> bool:
        """Whether or not the ot3-firmware builder container has local source mounted."""
        if self.firmware_builder is None:
            return False

        firmware_builder_mounts = get_mounts(self.firmware_builder)
        return (
            self.ot3_firmware_builder_created
            and firmware_builder_mounts is not None
            and any(
                mount.DEST_PATH == "/ot3-firmware" for mount in firmware_builder_mounts
            )
        )

    @property
    def ot3_firmware_build_args(self) -> "BuildArgConfigurations":
        """Returns BuildArgConfigurations object representing where source was pulled from."""
        return BuildArgConfigurations.parse_build_args(
            self.firmware_builder,
            "ot3-firmware/archive/refs/heads/main.zip",
            RepoToBuildArgMapping.OT3_FIRMWARE,
        )
