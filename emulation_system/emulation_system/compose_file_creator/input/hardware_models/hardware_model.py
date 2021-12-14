"""Parent class for all hardware."""
import os
import re
from typing import Dict, Any, Pattern

from pydantic import validator, BaseModel, Field

from emulation_system.compose_file_creator.config_file_settings import (
    SourceType,
    EmulationLevel,
)


class HardwareModel(BaseModel):
    """Parent class of all hardware. Define attributes common to all hardware."""

    _ID_REGEX_FORMAT: Pattern = re.compile(r"^[a-zA-Z0-9-_]+$")
    emulation_level: EmulationLevel = Field(alias="emulation-level")
    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")
    id: str

    class Config:
        """Config class used by pydantic."""

        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    @validator("id")
    def check_id_format(cls, v: str) -> str:
        """Verifies that id matches expected format."""
        assert cls._ID_REGEX_FORMAT.match(v), (
            f'"{v}" does not match required format of only alphanumeric characters, '
            f"dashes and underscores"
        )
        return v

    @validator("source_location")
    def check_source_location(cls, v: str, values: Dict[str, Any]) -> str:
        """If source type is local, confirms directory path specified exists."""
        if values["source_type"] == SourceType.LOCAL:
            assert os.path.isdir(v), f'"{v}" is not a valid directory path'
        return v
