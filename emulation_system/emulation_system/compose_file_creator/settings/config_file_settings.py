"""Defines all settings and constants for config file."""
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, DirectoryPath, Field, FilePath
from typing_extensions import Literal

ROOM_TEMPERATURE: float = 23.0

DEFAULT_DOCKER_COMPOSE_VERSION = "3.8"
DEFAULT_NETWORK_NAME = "local-network"
SOURCE_CODE_MOUNT_NAME = "SOURCE_CODE"
ROBOT_SERVER_MOUNT_NAME = "ROBOT_SERVER_SOURCE_CODE"
CAN_SERVER_MOUNT_NAME = "CAN_SERVER_SOURCE_CODE"
ENTRYPOINT_MOUNT_NAME = "ENTRYPOINT"
RESTRICTED_MOUNT_NAMES = [
    SOURCE_CODE_MOUNT_NAME,
    ROBOT_SERVER_MOUNT_NAME,
    ENTRYPOINT_MOUNT_NAME,
    CAN_SERVER_MOUNT_NAME,
]


class Hardware(str, Enum):
    """Names of supported hardware."""

    HEATER_SHAKER_MODULE = "heater-shaker-module"
    MAGNETIC_MODULE = "magnetic-module"
    THERMOCYCLER_MODULE = "thermocycler-module"
    TEMPERATURE_MODULE = "temperature-module"
    OT2 = "ot2"
    OT3 = "ot3"


class OT3Hardware(str, Enum):
    """Names of OT3 hardware."""

    PIPETTES = "ot3-pipettes"
    HEAD = "ot3-head"
    GANTRY_X = "ot3-gantry-x"
    GANTRY_Y = "ot3-gantry-y"
    BOOTLOADER = "ot3-bootloader"
    GRIPPER = "ot3-gripper"


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


class RepoToBuildArgMapping(str, Enum):
    """Build arg to use for specifying source download location."""

    OPENTRONS = "OPENTRONS_SOURCE_DOWNLOAD_LOCATION"
    OT3_FIRMWARE = "FIRMWARE_SOURCE_DOWNLOAD_LOCATION"
    OPENTRONS_MODULES = "MODULE_SOURCE_DOWNLOAD_LOCATION"


class SourceRepositories(BaseModel):
    """Stores names of source code repos for each piece of hardware."""

    firmware_repo_name: Optional[OpentronsRepository]
    hardware_repo_name: Optional[OpentronsRepository]


class MountTypes(str, Enum):
    """Possible mount types."""

    FILE = "file"
    DIRECTORY = "directory"


class Mount(BaseModel):
    """Contains infomation about a single extra bind mount."""

    name: str = Field(..., regex=r"^[A-Z0-9_]+$")
    type: str
    mount_path: str = Field(..., alias="mount-path")
    source_path: Union[DirectoryPath, FilePath] = Field(..., alias="source-path")

    def is_duplicate(self, other: "Mount") -> bool:
        """Compare everything except name."""
        return all(
            [
                self.type == other.type,
                self.mount_path == other.mount_path,
                self.source_path == other.source_path,
            ]
        )

    class Config:
        """Config class used by pydantic."""

        allow_population_by_field_name = True

    def get_bind_mount_string(self) -> str:
        """Return bind mount string to add compose file."""
        return f"{self.source_path}:{self.mount_path}"


class DirectoryMount(Mount):
    """Directory type Mount."""

    type: Literal[MountTypes.DIRECTORY]
    source_path: DirectoryPath = Field(..., alias="source-path")


class FileMount(Mount):
    """File type Mount."""

    type: Literal[MountTypes.FILE]
    source_path: FilePath = Field(..., alias="source-path")
