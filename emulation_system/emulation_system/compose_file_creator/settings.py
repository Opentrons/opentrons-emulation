from enum import Enum
from pydantic import BaseModel, Field

ROOM_TEMPERATURE: float = 23.0


class Hardware(str, Enum):
    """Hardware supported by emulation"""
    HEATER_SHAKER = "heater-shaker-module"
    THERMOCYCLER = "thermocycler-module"
    TEMPERATURE = "temperature-module"
    MAGNETEIC = "magnetic-module"
    OT2 = "ot2"
    OT3 = "ot3"


class EmulationLevel(str, Enum):
    """The emulation level of the emulator"""
    HARDWARE = "hardware"
    FIRMWARE = "firmware"


class SourceType(str, Enum):
    """Where to pull source from"""
    REMOTE = "remote"
    LOCAL = "local"


class HeaterShakerModes(str, Enum):
    """Where to read G-Codes from"""
    STDIN = "stdin"
    SOCKET = "socket"


class TemperatureModelSettings(BaseModel):
    """Temperature behavior model"""
    degrees_per_tick: float = Field(
        alias="degrees-per-tick", default=2.0
    )
    starting: float = float(ROOM_TEMPERATURE)


class PipetteSettings(BaseModel):
    """Pipette defintions for OT-2 and OT-3"""
    model: str = "p20_single_v2.0"
    id: str = "P20SV202020070101"