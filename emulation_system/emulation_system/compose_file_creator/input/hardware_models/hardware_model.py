"""Parent class for all hardware."""
from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.config_file_settings import (
    DirectoryMount,
    EmulationLevels,
    FileMount,
    Mount,
    SourceRepositories,
)
from emulation_system.compose_file_creator.images import get_image_name
from opentrons_pydantic_base_model import OpentronsBaseModel

from .hardware_specific_attributes import HardwareSpecificAttributes


class HardwareModel(OpentronsBaseModel):
    """Parent class of all hardware. Define attributes common to all hardware."""

    id: str = Field(..., regex=r"^[a-zA-Z0-9-_]+$")
    hardware: str
    # This is being called mounts because all mounts will be stored in it.
    # Just going to start by adding the extra-mounts to it and adding any
    # generated mounts during _post_init().
    mounts: List[Union[FileMount, DirectoryMount]] = Field(default=[])
    source_repos: SourceRepositories = NotImplemented
    emulation_level: EmulationLevels = NotImplemented
    hardware_specific_attributes: HardwareSpecificAttributes = NotImplemented

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    @validator("mounts")
    def check_for_duplicate_mounts(
        cls, v: List[Mount], values: Dict[str, Any]
    ) -> List[Mount]:
        """Confirms that there are not duplicate mounts."""
        assert all(
            [not mount_1 == mount_2 for mount_1, mount_2 in combinations(v, 2)]
        ), "Cannot have duplicate mounts"
        return v

    def get_image_name(self) -> str:
        """Get image name to run based off of passed parameters."""
        return get_image_name(self.hardware, self.emulation_level)

    def get_mount_strings(self) -> List[str]:
        """Get list of all mount strings for hardware."""
        mounts = [mount.get_bind_mount_string() for mount in self.mounts]
        return mounts

    def to_service(self) -> Service:
        """Converts HardwareModel object to Service object."""
        build = BuildItem(context=".", target=f"{self.get_image_name()}:latest")
        return Service(
            container_name=self.id,
            build=build,
            volumes=self.get_mount_strings(),  # type: ignore[arg-type]
            tty=True,
        )

    def get_hardware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for module when it is being emulated at hardware level."""
        return None

    def get_firmware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for module when it is being emulated at hardware level."""
        return None

    def is_firmware_emulation_level(self) -> bool:
        """Whether or not module is firmware emulation level."""
        return self.emulation_level == EmulationLevels.FIRMWARE

    def is_hardware_emulation_level(self) -> bool:
        """Whether or not module is hardware emulation level."""
        return self.emulation_level == EmulationLevels.HARDWARE
