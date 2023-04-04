"""Module containing helper class to access OT-3 Containers for local system"""

from dataclasses import dataclass
from typing import List, Optional

from docker.models.containers import Container  # type: ignore[import]

from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)
from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.helper_functions import get_mounts


@dataclass
class OT3Containers:
    """Dataclass to access all containers in OT-3 System easily."""

    gantry_x: Container
    gantry_y: Container
    head: Container
    gripper: Container
    pipettes: Container
    bootloader: Container
    state_manager: Container
    robot_server: Container
    can_server: Container
    emulator_proxy: Container

    # firmware and monorepo will actually always exist
    # but want to check that with an assert and not a type error
    firmware_builder: Optional[Container]
    monorepo_builder: Optional[Container]
    modules_builder: Optional[Container]

    @property
    def monorepo_builder_created(self) -> bool:
        """Whether or not the monorepo builder container was created."""
        return self.monorepo_builder is not None

    @property
    def local_monorepo_mounted(self) -> bool:
        """Whether or not the monorepo builder container has local source mounted."""
        if self.monorepo_builder is None:
            return False

        monorepo_builder_mounts = get_mounts(self.monorepo_builder)
        return (
            self.monorepo_builder_created
            and monorepo_builder_mounts is not None
            and any(
                mount["Destination"] == "/opentrons"
                for mount in monorepo_builder_mounts
            )
        )

    @property
    def monorepo_build_args(self) -> "BuildArgConfigurations":
        """Returns BuildArgConfigurations object representing where source was pulled from."""
        return BuildArgConfigurations.parse_build_args(
            self.monorepo_builder,
            "opentrons/archive/refs/heads/edge.zip",
            RepoToBuildArgMapping.OPENTRONS,
        )

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
                mount["Destination"] == "/ot3-firmware"
                for mount in firmware_builder_mounts
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

    @property
    def opentrons_modules_builder_created(self) -> bool:
        """Whether or not the opentrons-modules builder container was created."""
        return self.modules_builder is not None

    @property
    def local_opentrons_modules_mounted(self) -> bool:
        """Whether or not the opentrons-modules builder container has local source mounted."""
        if self.modules_builder is None:
            return False

        modules_builder_mounts = get_mounts(self.modules_builder)
        return (
            self.opentrons_modules_builder_created
            and modules_builder_mounts is not None
            and any(
                mount["Destination"] == "/opentrons-modules"
                for mount in modules_builder_mounts
            )
        )

    @property
    def opentrons_modules_build_args(self) -> "BuildArgConfigurations":
        """Returns BuildArgConfigurations object representing where source was pulled from."""
        return BuildArgConfigurations.parse_build_args(
            self.modules_builder,
            "opentrons-modules/archive/refs/heads/edge.zip",
            RepoToBuildArgMapping.OPENTRONS_MODULES,
        )

    @property
    def containers_with_entrypoint_script(self) -> List[Container]:
        """List of containers that are expected to have an entrypoint script."""
        return [
            self.gantry_x,
            self.gantry_y,
            self.head,
            self.gripper,
            self.pipettes,
            self.bootloader,
            self.state_manager,
            self.robot_server,
            self.can_server,
            self.emulator_proxy,
        ]

    @property
    def containers_with_monorepo_wheel_volume(self) -> List[Container]:
        """List of containers that are expected to have the monorepo wheel volume (/dist) folder."""
        return [
            self.monorepo_builder,
            self.emulator_proxy,
            self.robot_server,
            self.state_manager,
            self.can_server,
        ]
