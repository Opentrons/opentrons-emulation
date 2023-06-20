"""Defines all settings and constants for config file."""
from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Union

from pydantic import DirectoryPath, Field, FilePath
from typing_extensions import Literal

from emulation_system.consts import ROOM_TEMPERATURE
from emulation_system.github_api_interaction import check_if_branch_exists
from opentrons_pydantic_base_model import OpentronsBaseModel


class Hardware(str, Enum):
    """Names of supported hardware."""

    HEATER_SHAKER_MODULE = "heater-shaker-module"
    MAGNETIC_MODULE = "magnetic-module"
    THERMOCYCLER_MODULE = "thermocycler-module"
    TEMPERATURE_MODULE = "temperature-module"
    OT2 = "ot2"
    OT3 = "ot3"

    @classmethod
    def opentrons_modules_hardware(cls) -> List["Hardware"]:
        """Get names of of hardware that uses opentrons-modules repo."""
        return [cls.HEATER_SHAKER_MODULE, cls.THERMOCYCLER_MODULE]

    @property
    def hw_name(self) -> str:
        """Get name of hardware."""
        return self.value.replace("-module", "")

    @property
    def executable_volume_name(self) -> str:
        """Get name of volume that will be shared between services."""
        return f"{self.hw_name}-executable"

    @property
    def builder_executable_volume_path(self) -> str:
        """Where the builder container stores it's volumes."""
        return f"/volumes/{self.hw_name}-executable/"

    @property
    def simulator_name(self) -> str:
        """Generates simulator name."""
        return f'{self.value.replace("-module", "")}-simulator'


class OT3Hardware(str, Enum):
    """Names of OT3 hardware."""

    LEFT_PIPETTE = "ot3-left-pipette"
    RIGHT_PIPETTE = "ot3-right-pipette"
    HEAD = "ot3-head"
    GANTRY_X = "ot3-gantry-x"
    GANTRY_Y = "ot3-gantry-y"
    BOOTLOADER = "ot3-bootloader"
    GRIPPER = "ot3-gripper"

    @property
    def hw_name(self) -> str:
        """Get name of hardware."""
        return self.value.replace("ot3-", "")

    @property
    def builder_executable_volume_path(self) -> str:
        """Where the builder container stores its volumes."""
        return f"/volumes/{self.hw_name}-executable"

    @property
    def executable_volume_name(self) -> str:
        """Get name of volume that will share the built executable to the emulator."""
        return f"{self.hw_name}-executable"

    @property
    def eeprom_file_volume_name(self) -> str:
        """Get name of volume that will be share the generate eeprom.bin file into the emulator."""
        if self not in self.eeprom_required_hardware():
            raise ValueError(f"{self.value} does not require an eeprom file.")
        return f"{self.hw_name}-eeprom"

    @property
    def eeprom_file_volume_storage_path(self) -> str:
        """Path to eeprom file"""
        return f"/volumes/{self.hw_name}-eeprom"

    @property
    def simulator_name(self) -> str:
        """Generates simulator name."""
        return f'{self.value.replace("ot3-", "")}-simulator'

    @classmethod
    def eeprom_required_hardware(cls) -> List["OT3Hardware"]:
        """Get list of hardware that require eeprom file."""
        return [cls.LEFT_PIPETTE, cls.RIGHT_PIPETTE, cls.GRIPPER]


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


class TemperatureModelSettings(OpentronsBaseModel):
    """Temperature behavior model."""

    degrees_per_tick: float = Field(default=2.0)
    starting: float = float(ROOM_TEMPERATURE)


class RPMModelSettings(OpentronsBaseModel):
    """RPM behavior model."""

    rpm_per_tick: float = Field(default=100.0)
    starting: float = 0.0


class OpentronsRepository(str, Enum):
    """Possible repos to download from."""

    # Work-around for mypy to allow for custom __new__ method inside an enum
    if TYPE_CHECKING:
        value: str
        repo_name: str
        build_arg_name: str
        default_branch: str

    def __new__(
        cls, repo_name: str, build_args_name: str, default_branch: str
    ) -> "OpentronsRepository":
        """Initialize."""
        obj = str.__new__(cls, [repo_name])
        obj._value_ = repo_name
        obj.build_arg_name = build_args_name
        obj.default_branch = default_branch
        return obj

    OPENTRONS = ("opentrons", "OPENTRONS_SOURCE_DOWNLOAD_LOCATION", "edge")
    OT3_FIRMWARE = ("ot3-firmware", "FIRMWARE_SOURCE_DOWNLOAD_LOCATION", "main")
    OPENTRONS_MODULES = (
        "opentrons-modules",
        "MODULE_SOURCE_DOWNLOAD_LOCATION",
        "edge",
    )

    @property
    def OWNER(self) -> str:
        """Get owner of repo."""
        return "Opentrons"

    def _generate_download_url(self, owner: str, repo: str, branch: str) -> str:
        """Generate download url for source code."""
        return f"https://github.com/{owner}/{repo}.git#{branch}"

    def get_user_specified_download_url(self, branch: str) -> str:
        """Get download url for source code."""
        return self._generate_download_url(self.OWNER, self.value, branch)

    def get_default_download_url(self) -> str:
        """Get default download url for source code."""
        return self._generate_download_url(self.OWNER, self.value, self.default_branch)

    def check_if_branch_exists(self, branch: str) -> bool:
        """Check if branch exists."""
        return check_if_branch_exists(self.OWNER, self.value, branch)


class SourceRepositories(OpentronsBaseModel):
    """Stores names of source code repos for each piece of hardware."""

    firmware_repo_name: Optional[OpentronsRepository]
    hardware_repo_name: Optional[OpentronsRepository]


class MountTypes(str, Enum):
    """Possible mount types."""

    FILE = "file"
    DIRECTORY = "directory"


class Mount(OpentronsBaseModel):
    """Contains infomation about a single extra bind mount."""

    type: str
    mount_path: str
    source_path: Union[DirectoryPath, FilePath]

    def __eq__(self, other: object) -> bool:
        """Compare everything except name."""
        if not isinstance(other, Mount):
            return False

        return all(
            [
                self.type == other.type,
                self.mount_path == other.mount_path,
                self.source_path == other.source_path,
            ]
        )

    def get_bind_mount_string(self) -> str:
        """Return bind mount string to add compose file."""
        return f"{self.source_path}:{self.mount_path}"


class DirectoryMount(Mount):
    """Directory type Mount."""

    type: Literal[MountTypes.DIRECTORY]
    source_path: DirectoryPath


class FileMount(Mount):
    """File type Mount."""

    type: Literal[MountTypes.FILE]
    source_path: FilePath
