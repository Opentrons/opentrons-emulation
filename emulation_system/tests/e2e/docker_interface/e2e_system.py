"""Top-level class representing an entire emulated docker system."""

from dataclasses import dataclass
from typing import Optional

from docker.models.containers import Container  # type: ignore[import]

from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)

from ..test_definition.build_arg_configurations import BuildArgConfigurations
from e2e.consts import BindMountInfo
from e2e.helper_functions import get_mounts
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
    """Containers that will always exist in an emulated system."""

    robot_server: Container
    monorepo_builder: Container

    @property
    def monorepo_builder_created(self) -> bool:
        """Whether the monorepo builder container was created."""
        return self.monorepo_builder is not None

    @property
    def local_monorepo_mounted(self) -> bool:
        """Whether the monorepo builder container has local source mounted."""
        if self.monorepo_builder is None:
            return False

        monorepo_builder_mounts = get_mounts(self.monorepo_builder)
        return (
            self.monorepo_builder_created
            and monorepo_builder_mounts is not None
            and any(
                mount.DEST_PATH == "/opentrons" for mount in monorepo_builder_mounts
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
    """Top-level class containing the entire emulated robot."""

    default_containers: DefaultContainers
    ot3_containers: OT3SystemUnderTest
    module_containers: ModuleContainers
    expected_binds_mounts: ExpectedBindMounts
