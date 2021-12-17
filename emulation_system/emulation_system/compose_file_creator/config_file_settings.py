"""Defines all settings and constants for config file."""
from enum import Enum
from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)

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


class OpentronsRepository(str, Enum):
    """Possible repos to download from."""
    OPENTRONS = "opentrons"
    OT3_FIRMWARE = 'ot3-firmware'
    OPENTRONS_MODULES = 'opentrons-modules'


class Images(BaseModel):
    """Stores names of images for each piece of hardware."""
    local_firmware_image_name: Optional[str]
    local_hardware_image_name: Optional[str]
    remote_firmware_image_name: Optional[str]
    remote_hardware_image_name: Optional[str]


class SourceRepositories(BaseModel):
    """Stores names of source code repos for each piece of hardware."""
    firmware_repo_name: Optional[OpentronsRepository]
    hardware_repo_name: Optional[OpentronsRepository]
