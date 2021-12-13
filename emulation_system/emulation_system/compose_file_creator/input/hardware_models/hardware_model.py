import os
import re

from pydantic import validator, BaseModel, Field

from emulation_system.compose_file_creator.input.settings import (
    SourceType,
    EmulationLevel
)


class HardwareModel(BaseModel):
    """Parent class of all hardware. Provides access to attributes common to all
    hardware"""
    _ID_REGEX_FORMAT = re.compile(r"^[a-zA-Z0-9-_]+$")

    emulation_level: EmulationLevel = Field(alias="emulation-level")
    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")
    id: str

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    @validator("id")
    def check_id_format(cls, v):
        assert cls._ID_REGEX_FORMAT.match(v), (
            f"\"{v}\" does not match required format of only alphanumeric characters, "
            f"dashes and underscores"
        )
        return v

    @validator("source_location")
    def check_source_location(cls, v, values):
        if values['source_type'] == SourceType.LOCAL:
            assert os.path.isdir(v), f"\"{v}\" is not a valid directory path"
        return v
