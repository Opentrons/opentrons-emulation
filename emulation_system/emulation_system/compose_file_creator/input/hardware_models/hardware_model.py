"""Parent class for all hardware."""
from __future__ import annotations

import os
from typing import (
    Any,
    Dict,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    validator,
)

from emulation_system.compose_file_creator.settings.config_file_settings import (
    DirectoryExtraMount,
    EmulationLevels,
    FileExtraMount,
    SourceRepositories,
    SourceType,
    ExtraMount,
)


class NoMountsDefinedException(Exception):
    """Exception thrown when you try to load a mount and none are defined."""

    pass


class HardwareModel(BaseModel):
    """Parent class of all hardware. Define attributes common to all hardware."""

    id: str = Field(..., regex=r"^[a-zA-Z0-9-_]+$")
    hardware: str
    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")
    extra_mounts: Dict[str, Union[FileExtraMount, DirectoryExtraMount]] = Field(
        alias="extra-mounts", default={}
    )

    source_repos: SourceRepositories = NotImplemented
    emulation_level: EmulationLevels = NotImplemented

    class Config:
        """Config class used by pydantic."""

        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    @validator("extra_mounts", pre=True)
    def add_extra_mounts_names(cls, value) -> Dict[str, ExtraMount]:  # noqa: ANN001
        """Adds names from dict to ExtraMount object."""
        for key, mount in value.items():
            mount["name"] = key
        return value

    @validator("source_location")
    def check_source_location(cls, v: str, values: Dict[str, Any]) -> str:
        """If source type is local, confirms directory path specified exists."""
        if values["source_type"] == SourceType.LOCAL:
            assert os.path.isdir(v), f'"{v}" is not a valid directory path'
        return v

    def get_mount_by_name(self, name: str) -> ExtraMount:
        """Lookup and return ExtraMount by name."""
        if len(self.extra_mounts) == 0:
            raise NoMountsDefinedException("You have no mounts defined.")
        else:
            return self.extra_mounts[name]
