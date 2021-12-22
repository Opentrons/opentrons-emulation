"""Defines all settings and constants for config file."""
from enum import Enum
from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    DirectoryPath,
    Field,
    FilePath,
)
from typing_extensions import Literal

ROOM_TEMPERATURE: float = 23.0


class Hardware(str, Enum):
    """Names of supported hardware."""

    HEATER_SHAKER_MODULE = "heater-shaker-module"
    MAGNETIC_MODULE = "magnetic-module"
    THERMOCYCLER_MODULE = "thermocycler-module"
    TEMPERATURE_MODULE = "temperature-module"
    OT2 = "ot2"
    OT3 = "ot3"


class EmulationLevels(str, Enum):
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
    OT3_FIRMWARE = "ot3-firmware"
    OPENTRONS_MODULES = "opentrons-modules"


class SourceRepositories(BaseModel):
    """Stores names of source code repos for each piece of hardware."""

    firmware_repo_name: Optional[OpentronsRepository]
    hardware_repo_name: Optional[OpentronsRepository]


class MountTypes(str, Enum):
    """Possible mount types."""

    FILE = "file"
    DIRECTORY = "directory"


class ExtraMount(BaseModel):
    """Contains infomation about a single extra bind mount."""

    type: str
    name: str = Field(..., regex=r"^[A-Z0-9_]+$")
    mount_path: str = Field(..., alias="mount-path")


class DirectoryExtraMount(ExtraMount):
    """Directory type ExtraMount."""

    type: Literal[MountTypes.DIRECTORY]
    source_path: DirectoryPath = Field(..., alias="source-path")


class FileExtraMount(ExtraMount):
    """File type ExtraMount."""

    type: Literal[MountTypes.FILE]
    source_path: FilePath = Field(..., alias="source-path")
