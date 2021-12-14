"""Parent class for all attributes specific to individual pieces of hardware."""
from pydantic import BaseModel


class HardwareSpecificAttributes(BaseModel):
    """Parent class for all attributes specific to individual pieces of hardware."""

    class Config:
        """Config class used by pydantic."""

        extra = "forbid"
