from pydantic import BaseModel


class HardwareSpecificAttributes(BaseModel):

    class Config:
        extra = "forbid"

