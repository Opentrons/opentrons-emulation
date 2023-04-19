from dataclasses import dataclass
from typing import List, Optional

from docker.models.containers import Container  # type: ignore[import]

from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)

from ..test_definition.build_arg_configurations import BuildArgConfigurations
from ..utilities.consts import BindMountInfo
from ..utilities.helper_functions import get_mounts
from .module_containers import ModuleContainers
from .ot3_containers import OT3SystemUnderTest


@dataclass
class ExpectedBindMounts:
    """Helper class containing expected bind mounts for e2e test."""

    MONOREPO: Optional[BindMountInfo]
    FIRMWARE: Optional[BindMountInfo]
    MODULES: Optional[BindMountInfo]


@dataclass
class DefaultContainers:
    robot_server: Container
    monorepo_builder: Container

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
                mount.DEST_PATH == "/opentrons"
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


@dataclass
class E2EHostSystem:
    default_containers: DefaultContainers
    ot3_containers: OT3SystemUnderTest
    module_containers: ModuleContainers
    expected_binds_mounts: ExpectedBindMounts

    @property
    def containers_with_entrypoint_script(self) -> List[Container]:
        return [
            self.ot3_containers.gantry_x,
            self.ot3_containers.gantry_y,
            self.ot3_containers.head,
            self.ot3_containers.gripper,
            self.ot3_containers.pipettes,
            self.ot3_containers.bootloader,
            self.ot3_containers.state_manager,
            self.ot3_containers.can_server,
            self.default_containers.robot_server,
        ]

    # @property
    # def containers_with_monorepo_wheel_volume(self) -> List[Container]:
    #     """List of containers that are expected to have the monorepo wheel volume (/dist) folder."""
    #     return [
    #         self.monorepo_builder,
    #         self.robot_server,
    #         self.state_manager,
    #         self.can_server,
    #     ]
