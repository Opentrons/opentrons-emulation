"""Override Pydantic's BaseModel to globally do the following:

- use kebab case for field names.
- forbid extra fields.
- allow population by field name.
- use enum values.
- validate assignment.
"""

from pydantic import BaseModel as PydanticBaseModel


def to_kebab(string: str) -> str:
    """Converts snake case formatted string to kebab case."""
    return string.replace("_", "-")

class OpentronsBaseModel(PydanticBaseModel):
    """Override Pydantic Base Model with custom config."""
    class Config:  # noqa: D106
        alias_generator = to_kebab
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True
        validate_assignment = True
