from pydantic import BaseModel as PydanticBaseModel

def to_kebab(string: str) -> str:
    """Converts snake case formatted string to kebab case."""
    return string.replace("_", "-")

class OpentronsBaseModel(PydanticBaseModel):
    class Config:
        alias_generator = to_kebab
        extra = "forbid"
        allow_population_by_field_name = True
        use_enum_values = True
        validate_assignment = True
