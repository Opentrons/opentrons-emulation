"""Parent class for all hardware."""
from __future__ import annotations

import os
import pathlib
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    validator,
)

from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Service,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DirectoryMount,
    EmulationLevels,
    FileMount,
    Mount,
    MountTypes,
    OpentronsRepository,
    SourceRepositories,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import IMAGE_MAPPING


class NoMountsDefinedException(Exception):
    """Exception thrown when you try to load a mount and none are defined."""

    pass


class MountNotFoundException(Exception):
    """Exception thrown when mount of a certain name is not found."""

    pass


class EmulationLevelNotSupportedError(Exception):
    """Exception thrown when emulation level is not supported."""

    pass


class HardwareModel(BaseModel):
    """Parent class of all hardware. Define attributes common to all hardware."""

    id: str = Field(..., regex=r"^[a-zA-Z0-9-_]+$")
    hardware: str
    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")
    # This is being called mounts because all mounts will be stored in it.
    # Just going to start by adding the extra-mounts to it and adding any
    # generated mounts during _post_init().
    mounts: List[Union[FileMount, DirectoryMount]] = Field(
        alias="extra-mounts", default=[]
    )

    source_repos: SourceRepositories = NotImplemented
    emulation_level: EmulationLevels = NotImplemented

    class Config:
        """Config class used by pydantic."""

        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._post_init()

    def _post_init(self) -> None:
        """Methods to always run after initialization."""
        self._add_source_bind_mount()

    def _add_source_bind_mount(self) -> None:
        """If running a local type image add the mount to the mounts attribute."""
        if self.source_type == SourceType.LOCAL:
            self.mounts.append(
                DirectoryMount(
                    name="SOURCE_CODE",
                    type=MountTypes.DIRECTORY,
                    source_path=pathlib.Path(self.source_location),
                    mount_path=f"/{self.get_source_repo()}",
                )
            )

    @validator("source_location")
    def check_source_location(cls, v: str, values: Dict[str, Any]) -> str:
        """If source type is local, confirms directory path specified exists."""
        if values["source_type"] == SourceType.LOCAL:
            assert os.path.isdir(v), f'"{v}" is not a valid directory path'
        return v

    def get_mount_by_name(self, name: str) -> Mount:
        """Lookup and return Mount by name."""
        if len(self.mounts) == 0:
            raise NoMountsDefinedException("You have no mounts defined.")
        else:
            found_mounts = [mount for mount in self.mounts if mount.name == name]

            if len(found_mounts) == 0:
                raise MountNotFoundException(f'Mount named "{name}" not found.')
            else:
                return found_mounts[0]

    def get_source_repo(self) -> OpentronsRepository:
        """Get source repo for HardwareModel."""
        if self.emulation_level == EmulationLevels.HARDWARE:
            repo = self.source_repos.hardware_repo_name
        else:
            repo = self.source_repos.firmware_repo_name

        if repo is None:
            raise EmulationLevelNotSupportedError(
                f'Emulation level, "{self.emulation_level}" not supported for '
                f"{self.hardware}"
            )

        return repo

    def get_image_name(self) -> Optional[str]:
        """Get image name to run based off of passed parameters."""
        image = IMAGE_MAPPING[self.hardware]
        comp_tuple = (self.source_type, self.emulation_level)

        if comp_tuple == (SourceType.REMOTE, EmulationLevels.HARDWARE):
            image_name = image.remote_hardware_image_name
        elif comp_tuple == (SourceType.REMOTE, EmulationLevels.FIRMWARE):
            image_name = image.remote_firmware_image_name
        elif comp_tuple == (SourceType.LOCAL, EmulationLevels.HARDWARE):
            image_name = image.local_hardware_image_name
        else:  # (SourceType.LOCAL, EmulationLevels.FIRMWARE)
            image_name = image.local_firmware_image_name

        return image_name

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
