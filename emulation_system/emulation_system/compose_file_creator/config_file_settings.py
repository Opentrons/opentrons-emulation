"""Defines all settings and constants for config file."""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

ROOM_TEMPERATURE: float = 23.0


class EmulationLevel(str, Enum):
    """The emulation level of the emulator."""

    HARDWARE = "hardware"
    FIRMWARE = "firmware"


class SourceType(str, Enum):
    """Where to pull source from."""

    REMOTE = "remote"
    LOCAL = "local"


class HeaterShakerModes(str, Enum):
    """Where to read G-Codes from."""

    STDIN = "stdin"
    SOCKET = "socket"


class TemperatureModelSettings(BaseModel):
    """Temperature behavior model."""

    degrees_per_tick: float = Field(alias="degrees-per-tick", default=2.0)
    starting: float = float(ROOM_TEMPERATURE)


class PipetteSettings(BaseModel):
    """Pipette defintions for OT-2 and OT-3."""

    model: str = "p20_single_v2.0"
    id: str = "P20SV202020070101"


class SourceLocation(str, Enum):
    """Possible repos to download from."""
    OPENTRONS = "opentrons"
    OT3_FIRMWARE = 'ot3-firmware'
    OPENTRONS_MODULES = 'opentrons-modules'


class HardwareDefinition(Enum):
    """Hardware supported by emulation."""

    HEATER_SHAKER = ("heater-shaker-module", None, SourceLocation.OPENTRONS_MODULES)
    THERMOCYCLER = (
        "thermocycler-module",
        SourceLocation.OPENTRONS,
        SourceLocation.OPENTRONS_MODULES
    )
    TEMPERATURE = (
        "temperature-module",
        SourceLocation.OPENTRONS,
        SourceLocation.OPENTRONS_MODULES
    )
    MAGNETIC = (
        "magnetic-module",
        SourceLocation.OPENTRONS,
        SourceLocation.OPENTRONS_MODULES
    )
    OT2 = ('ot2', SourceLocation.OPENTRONS, None)
    OT3 = ('ot3', None, None)

    def __init__(
        self,
        id: str,
        firmware_source: Optional[SourceLocation],
        hardware_source: Optional[SourceLocation]
    ) -> None:
        self._id = id
        self._firmware_source = firmware_source
        self._hardware_source = hardware_source

    @property
    def id(self) -> str:
        """Get id of hardware."""
        return self._id

    def get_source_repo(self, level: EmulationLevel) -> Optional[str]:
        """Get source repo from hardware type and level."""
        if level == EmulationLevel.FIRMWARE.value:
            source = self._firmware_source
        elif level == EmulationLevel.HARDWARE.value:
            source = self._hardware_source
        else:
            raise ValueError(
                f"\"{level}\" is not a valid level. "
                f"Valid levels are"
            )
        if source is not None:
            source = source.value

        return source


if __name__ == "__main__":
    print(HardwareDefinition.HEATER_SHAKER.get_source_repo('hardware'))
