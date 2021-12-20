"""Parent class for all hardware."""
from __future__ import annotations

import os
from typing import (
    Any,
    Dict,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
    validator,
)

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Images,
    SourceRepositories,
    SourceType,
)


class HardwareModel(BaseModel):
    """Parent class of all hardware. Define attributes common to all hardware."""

    id: str = Field(..., regex=r"^[a-zA-Z0-9-_]+$")
    hardware: str
    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")

    # Should be overriden in child classes
    images: Images = NotImplemented
    source_repos: SourceRepositories = NotImplemented
    emulation_level: EmulationLevels = NotImplemented

    class Config:
        """Config class used by pydantic."""

        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    @validator("source_location")
    def check_source_location(cls, v: str, values: Dict[str, Any]) -> str:
        """If source type is local, confirms directory path specified exists."""
        if values["source_type"] == SourceType.LOCAL:
            assert os.path.isdir(v), f'"{v}" is not a valid directory path'
        return v

    def get_image_name(self) -> Optional[str]:
        """Get image name to run based off of class structure."""
        if (
            self.emulation_level == EmulationLevels.HARDWARE
            and self.source_type == SourceType.REMOTE
        ):
            image_name = self.images.remote_hardware_image_name

        elif (
            self.emulation_level == EmulationLevels.HARDWARE
            and self.source_type == SourceType.LOCAL
        ):
            image_name = self.images.local_hardware_image_name

        elif (
            self.emulation_level == EmulationLevels.FIRMWARE
            and self.source_type == SourceType.REMOTE
        ):
            image_name = self.images.remote_firmware_image_name

        else:
            image_name = self.images.local_firmware_image_name

        return image_name

    def get_source_repo(self) -> str:
        """Get name of Docker image to use."""
        return "Hello World"
