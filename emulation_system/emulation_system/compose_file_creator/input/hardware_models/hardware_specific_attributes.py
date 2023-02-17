"""Parent class for all attributes specific to individual pieces of hardware."""
from pydantic import BaseModel

from emulation_system.compose_file_creator.utilities.shared_functions import to_kebab


class HardwareSpecificAttributes(BaseModel):
    """Parent class for all attributes specific to individual pieces of hardware."""

    class Config:
        """Config class used by pydantic."""

        extra = "forbid"
        alias_generator = to_kebab
        allow_population_by_field_name = True
