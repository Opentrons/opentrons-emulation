"""Dataclasses representing constants for e2e tests.

All dataclasses should be declared as frozen
"""
from dataclasses import dataclass

from emulation_system.consts import (
    EMULATOR_STATE_MANAGER_VENV_NAMED_VOLUME_STRING,
    EMULATOR_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING,
    ENTRYPOINT_FILE_LOCATION,
    MONOREPO_NAMED_VOLUME_STRING,
    OPENTRONS_MODULES_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME,
    OPENTRONS_MODULES_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME,
    OT3_FIRMWARE_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME,
    OT3_FIRMWARE_BUILDER_STATE_MANAGER_VENV_NAMED_VOLUME_STRING,
    OT3_FIRMWARE_BUILDER_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING,
    OT3_FIRMWARE_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME,
)


@dataclass(frozen=True)
class NamedVolumeInfo:
    """Dataclass representing expected named volume for a container."""

    VOLUME_NAME: str
    DEST_PATH: str

    @classmethod
    def from_string(cls, string: str) -> "NamedVolumeInfo":
        """Build NamedVolumeInfo class from docker syntax string."""
        return cls(*string.split(":"))


@dataclass(frozen=True)
class BindMountInfo:
    """Dataclass representing expected mount for a container."""

    SOURCE_PATH: str
    DEST_PATH: str


STATE_MANAGER_VENV_VOLUME = NamedVolumeInfo.from_string(
    EMULATOR_STATE_MANAGER_VENV_NAMED_VOLUME_STRING
)
STATE_MANAGER_WHEEL_VOLUME = NamedVolumeInfo.from_string(
    EMULATOR_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING
)
ENTRYPOINT_MOUNT = BindMountInfo(ENTRYPOINT_FILE_LOCATION, "/entrypoint.sh")
MONOREPO_WHEEL_VOLUME = NamedVolumeInfo.from_string(MONOREPO_NAMED_VOLUME_STRING)
OT3_FIRMWARE_BUILDER_NAMED_VOLUMES = {
    NamedVolumeInfo.from_string(OT3_FIRMWARE_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME),
    NamedVolumeInfo.from_string(
        OT3_FIRMWARE_BUILDER_STATE_MANAGER_VENV_NAMED_VOLUME_STRING
    ),
    NamedVolumeInfo.from_string(
        OT3_FIRMWARE_BUILDER_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING
    ),
    NamedVolumeInfo.from_string(OT3_FIRMWARE_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME),
    NamedVolumeInfo("bootloader-executable", "/volumes/bootloader-executable"),
    NamedVolumeInfo("gantry-x-executable", "/volumes/gantry-x-executable"),
    NamedVolumeInfo("gantry-y-executable", "/volumes/gantry-y-executable"),
    NamedVolumeInfo("gripper-eeprom", "/volumes/gripper-eeprom"),
    NamedVolumeInfo("gripper-executable", "/volumes/gripper-executable"),
    NamedVolumeInfo("head-executable", "/volumes/head-executable"),
    NamedVolumeInfo("left-pipette-eeprom", "/volumes/left-pipette-eeprom"),
    NamedVolumeInfo("left-pipette-executable", "/volumes/left-pipette-executable"),
    NamedVolumeInfo("right-pipette-eeprom", "/volumes/right-pipette-eeprom"),
    NamedVolumeInfo("right-pipette-executable", "/volumes/right-pipette-executable"),
}

OPENTRONS_MODULES_BUILDER_NAMED_VOLUMES = {
    NamedVolumeInfo.from_string(
        OPENTRONS_MODULES_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME
    ),
    NamedVolumeInfo.from_string(
        OPENTRONS_MODULES_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME
    ),
    NamedVolumeInfo("heater-shaker-executable", "/volumes/heater-shaker-executable"),
    NamedVolumeInfo("thermocycler-executable", "/volumes/thermocycler-executable"),
}


@dataclass(frozen=True)
class OT3FirmwareEmulatorNamedVolumesMap:
    """Class representing expected named volume for each OT-3 emulator container."""

    BOOTLOADER = NamedVolumeInfo("bootloader-executable", "/executable")
    GANTRY_X = NamedVolumeInfo("gantry-x-executable", "/executable")
    GANTRY_Y = NamedVolumeInfo("gantry-y-executable", "/executable")
    GRIPPER = {
        NamedVolumeInfo("gripper-executable", "/executable"),
        NamedVolumeInfo("gripper-eeprom", "/eeprom"),
    }
    HEAD = NamedVolumeInfo("head-executable", "/executable")
    LEFT_PIPETTE = {
        NamedVolumeInfo("left-pipette-executable", "/executable"),
        NamedVolumeInfo("left-pipette-eeprom", "/eeprom"),
    }
    RIGHT_PIPETTE = {
        NamedVolumeInfo("right-pipette-executable", "/executable"),
        NamedVolumeInfo("right-pipette-eeprom", "/eeprom"),
    }


@dataclass(frozen=True)
class OpentronsModulesEmulatorNamedVolumes:
    """Expected named volumes for opentrons-modules emulator containers."""

    HEATER_SHAKER = NamedVolumeInfo("heater-shaker-executable", "/executable")
    THERMOCYCLER = NamedVolumeInfo("thermocycler-executable", "/executable")


@dataclass(frozen=True)
class OT3FirmwareExpectedBinaryNames:
    """Exepected names of OT-3 Firmware binary executables."""

    BOOTLOADER = "bootloader-simulator"
    GANTRY_X = "gantry-x-simulator"
    GANTRY_Y = "gantry-y-simulator"
    GRIPPER = "gripper-simulator"
    HEAD = "head-simulator"
    LEFT_PIPETTE = {
        "pipettes-96-simulator",
        "pipettes-multi-simulator",
        "pipettes-single-simulator",
    }
    RIGHT_PIPETTE = {
        "pipettes-96-simulator",
        "pipettes-multi-simulator",
        "pipettes-single-simulator",
    }


@dataclass(frozen=True)
class ModulesExpectedBinaryNames:
    """Expecte names of opentrons-modules binary executableds."""

    HEATER_SHAKER = "heater-shaker-simulator"
    THERMOCYCLER = "thermocycler-simulator"
