from pydantic import BaseModel


class HardwareSpecificAttributes(BaseModel):
    """Parent class for all attributes specific to individual pieces of hardware"""
    class Config:
        extra = "forbid"

