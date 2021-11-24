from pydantic import BaseModel, Field
from typing_extensions import Literal

from compose_file_creator.input.settings import (
    EmulationLevel,
    SourceType
)


class BaseAttributes(BaseModel):
    emulation_level: EmulationLevel = Field(alias="emulation-level")
    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")

    def __init_subclass__(cls, **kwargs):
        try:
            cls.__fields__['hardware'].outer_type_
        except KeyError:
            raise TypeError(f"Class {cls.__name__!r} needs field 'hardware'")

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        extra = "forbid"
