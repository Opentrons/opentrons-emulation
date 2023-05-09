"""Dataclasses representing constants for e2e tests.

All dataclasses should be declared as frozen
"""
from dataclasses import dataclass

from emulation_system.consts import (
    EMULATOR_STATE_MANAGER_VENV_NAMED_VOLUME_STRING,
    EMULATOR_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING,
    ENTRYPOINT_FILE_LOCATION,
    MONOREPO_NAMED_VOLUME_STRING,
    OT3_FIRMWARE_BUILDER_STATE_MANAGER_VENV_NAMED_VOLUME_STRING,
    OT3_FIRMWARE_BUILDER_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING,
    OPENTRONS_MODULES_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME,
    OPENTRONS_MODULES_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME, OT3_FIRMWARE_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME,
    OT3_FIRMWARE_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME,
)


@dataclass(frozen=True)
class NamedVolumeInfo:
    """Dataclass representing expected named volume for a container."""

    VOLUME_NAME: str
    DEST_PATH: str

    @classmethod
    def from_string(cls, string: str) -> "NamedVolumeInfo":
        return cls(*string.split(":"))


@dataclass(frozen=True)
class BindMountInfo:
    """Dataclass representing expected mount for a container"""

    SOURCE_PATH: str
    DEST_PATH: str

    def __hash__(self):
        return hash((self.SOURCE_PATH, self.DEST_PATH))


STATE_MANAGER_VENV_VOLUME = NamedVolumeInfo.from_string(
    EMULATOR_STATE_MANAGER_VENV_NAMED_VOLUME_STRING
)
STATE_MANAGER_WHEEL_VOLUME = NamedVolumeInfo.from_string(
    EMULATOR_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING
)
ENTRYPOINT_MOUNT = BindMountInfo(ENTRYPOINT_FILE_LOCATION, "/entrypoint.sh")
MONOREPO_WHEEL_VOLUME = NamedVolumeInfo.from_string(MONOREPO_NAMED_VOLUME_STRING)
OT3_FIRMWARE_BUILDER_NAMED_VOLUMES = {
    NamedVolumeInfo("gantry-x-executable", "/volumes/gantry-x-volume"),
    NamedVolumeInfo("gantry-y-executable", "/volumes/gantry-y-volume"),
    NamedVolumeInfo("head-executable", "/volumes/head-volume"),
    NamedVolumeInfo("gripper-executable", "/volumes/gripper-volume"),
    NamedVolumeInfo("pipettes-executable", "/volumes/pipettes-volume"),
    NamedVolumeInfo("bootloader-executable", "/volumes/bootloader-volume"),
    NamedVolumeInfo.from_string(
        OT3_FIRMWARE_BUILDER_STATE_MANAGER_VENV_NAMED_VOLUME_STRING
    ),
    NamedVolumeInfo.from_string(
        OT3_FIRMWARE_BUILDER_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING
    ),
    NamedVolumeInfo.from_string(
        OT3_FIRMWARE_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME
    ),
    NamedVolumeInfo.from_string(
        OT3_FIRMWARE_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME
    ),
}

OPENTRONS_MODULES_BUILDER_NAMED_VOLUMES = {
    NamedVolumeInfo(
        "heater-shaker-executable", "/volumes/heater-shaker-volume"
    ),
    NamedVolumeInfo(
        "thermocycler-executable", "/volumes/thermocycler-volume"
    ),
    NamedVolumeInfo.from_string(OPENTRONS_MODULES_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME),
    NamedVolumeInfo.from_string(OPENTRONS_MODULES_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME)
}


@dataclass(frozen=True)
class OT3FirmwareEmulatorNamedVolumesMap:
    """Class representing expected named volume for each OT-3 emulator container."""

    GANTRY_X = NamedVolumeInfo("gantry-x-executable", "/executable")
    GANTRY_Y = NamedVolumeInfo("gantry-y-executable", "/executable")
    HEAD = NamedVolumeInfo("head-executable", "/executable")
    GRIPPER = NamedVolumeInfo("gripper-executable", "/executable")
    PIPETTES = NamedVolumeInfo("pipettes-executable", "/executable")
    BOOTLOADER = NamedVolumeInfo("bootloader-executable", "/executable")


@dataclass(frozen=True)
class OpentronsModulesEmulatorNamedVolumes:
    """Expected named volumes for opentrons-modules emulator containers."""

    HEATER_SHAKER = NamedVolumeInfo("heater-shaker-executable", "/executable")
    THERMOCYCLER = NamedVolumeInfo("thermocycler-executable", "/executable")


@dataclass(frozen=True)
class OT3FirmwareExpectedBinaryNames:
    """Exepected names of OT-3 Firmware binary executables."""

    GANTRY_X = "gantry-x-simulator"
    GANTRY_Y = "gantry-y-simulator"
    HEAD = "head-simulator"
    GRIPPER = "gripper-simulator"
    PIPETTES = "pipettes-simulator"
    BOOTLOADER = "bootloader-simulator"


@dataclass(frozen=True)
class ModulesExpectedBinaryNames:
    """Expecte names of opentrons-modules binary executableds"""

    THERMOCYCLER = "thermocycler-simulator"
    HEATER_SHAKER = "heater-shaker-simulator"
