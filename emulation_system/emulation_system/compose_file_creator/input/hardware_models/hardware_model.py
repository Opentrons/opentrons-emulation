"""Parent class for all hardware."""
from __future__ import annotations

import os
import pathlib
import re
from typing import (
    Any,
    Dict,
    List,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    validator,
)

from emulation_system.compose_file_creator.errors import (
    EmulationLevelNotSupportedError,
    InvalidRemoteSourceError,
    LocalSourceDoesNotExistError,
    MountNotFoundError,
    NoMountsDefinedError,
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
    RESTRICTED_MOUNT_NAMES,
    SOURCE_CODE_MOUNT_NAME,
    SourceRepositories,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import (
    get_image_name,
)

COMMIT_SHA_REGEX = r"^[0-9a-f]{40}"


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
                    name=SOURCE_CODE_MOUNT_NAME,
                    type=MountTypes.DIRECTORY,
                    source_path=pathlib.Path(self.source_location),
                    mount_path=f"/{self.get_source_repo()}",
                )
            )

    @validator("source_location")
    def check_source_location(cls, v: str, values: Dict[str, Any]) -> str:
        """If source type is local, confirms directory path specified exists."""
        if values["source_type"] == SourceType.LOCAL:
            if not os.path.isdir(v):
                raise LocalSourceDoesNotExistError(v)
        else:
            if v != "latest" and re.compile(COMMIT_SHA_REGEX).match(v) is None:
                raise InvalidRemoteSourceError(v)
        return v

    @validator("mounts", pre=True, each_item=True)
    def check_for_restricted_names(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Confirms that none of the mount names use restricted values."""
        assert v["name"] not in RESTRICTED_MOUNT_NAMES, (
            "Mount name cannot be any of the following values: "
            f"{', '.join(RESTRICTED_MOUNT_NAMES)}"
        )
        return v

    @validator("mounts")
    def check_for_duplicate_mount_names(
        cls, v: List[Mount], values: Dict[str, Any]
    ) -> List[Mount]:
        """Confirms that there are not mounts with duplicate names."""
        names = [mount.name for mount in v]
        assert len(names) == len(
            set(names)
        ), f"\"{values['id']}\" has mounts with duplicate names"
        return v

    def get_mount_by_name(self, name: str) -> Mount:
        """Lookup and return Mount by name."""
        if len(self.mounts) == 0:
            raise NoMountsDefinedError
        else:
            found_mounts = [mount for mount in self.mounts if mount.name == name]

            if len(found_mounts) == 0:
                raise MountNotFoundError(name)
            else:
                return found_mounts[0]

    def get_source_repo(self) -> OpentronsRepository:
        """Get source repo for HardwareModel."""
        if self.emulation_level == EmulationLevels.HARDWARE:
            repo = self.source_repos.hardware_repo_name
        else:
            repo = self.source_repos.firmware_repo_name

        if repo is None:
            raise EmulationLevelNotSupportedError(self.emulation_level, self.hardware)

        return repo

    def get_image_name(self) -> str:
        """Get image name to run based off of passed parameters."""
        return get_image_name(self.hardware, self.source_type, self.emulation_level)

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
