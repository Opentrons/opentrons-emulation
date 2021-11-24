from enum import Enum
from pydantic import BaseModel, Field

ROOM_TEMPERATURE = 23


class Hardware(str, Enum):
    HEATER_SHAKER_MODULE = "Heater Shaker Module"
    THERMOCYCLER_MODULE = "Thermocycler Module"
    TEMPERATURE_MODULE = "Temperature Module"
    MAGNETEIC_MODULE = "Magnetic Module"
    OT2 = "OT-2"
    OT3 = "OT-3"


class EmulationLevel(str, Enum):
    FIRMWARE = "firmware"
    DRIVER = "driver"


class SourceType(str, Enum):
    REMOTE = "remote"
    LOCAL = "local"


class HeaterShakerModes(str, Enum):
    STDIN = "stdin"
    SOCKET = "socket"


class TemperatureModelSettings(BaseModel):
    degrees_per_tick: float = Field(
        alias="degrees-per-tick", default=2.0
    )
    starting: float = float(ROOM_TEMPERATURE)

