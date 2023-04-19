"""Dataclasses representing constants for e2e tests.

All dataclasses should be declared as frozen
"""
import os
from dataclasses import dataclass

from emulation_system.consts import DOCKERFILE_DIR_LOCATION


@dataclass(frozen=True)
class NamedVolumeInfo:
    """Dataclass representing expected named volume for a container."""

    VOLUME_NAME: str
    DEST_PATH: str


@dataclass(frozen=True)
class BindMountInfo:
    """Dataclass representing expected mount for a container"""

    SOURCE_PATH: str
    DEST_PATH: str


STATE_MANAGER_VENV_VOLUME = NamedVolumeInfo("state_manager_venv", "/.venv")
ENTRYPOINT_MOUNT = BindMountInfo(
    os.path.join(DOCKERFILE_DIR_LOCATION, "entrypoint.sh"), "/entrypoint.sh"
)
MONOREPO_WHEELS = NamedVolumeInfo("monorepo-wheels", "/dist")
OT3_FIRMWARE_NAMED_VOLUMES = {
    NamedVolumeInfo("gantry_x_executable", "/volumes/gantry_x_volume"),
    NamedVolumeInfo("gantry_y_executable", "/volumes/gantry_y_volume"),
    NamedVolumeInfo("head_executable", "/volumes/head_volume"),
    NamedVolumeInfo("gripper_executable", "/volumes/gripper_volume"),
    NamedVolumeInfo("pipettes_executable", "/volumes/pipettes_volume"),
    NamedVolumeInfo("bootloader_executable", "/volumes/bootloader_volume"),
    NamedVolumeInfo("state_manager_venv", "/ot3-firmware/build-host/.venv"),
}


@dataclass(frozen=True)
class OT3FirmwareEmulatorNamedVolumesMap:
    """Class representing expected named volume for each OT-3 emulator container."""

    GANTRY_X = NamedVolumeInfo("gantry_x_executable", "/executable")
    GANTRY_Y = NamedVolumeInfo("gantry_y_executable", "/executable")
    HEAD = NamedVolumeInfo("head_executable", "/executable")
    GRIPPER = NamedVolumeInfo("gripper_executable", "/executable")
    PIPETTES = NamedVolumeInfo("pipettes_executable", "/executable")
    BOOTLOADER = NamedVolumeInfo("bootloader_executable", "/executable")


@dataclass(frozen=True)
class OpentronsModulesBuilderNamedVolumesMap:
    """Expected named volumes for opentrons-modules builder container."""

    HEATER_SHAKER = NamedVolumeInfo(
        "heater_shaker_executable", "/volumes/heater_shaker_volume"
    )
    THERMOCYCLER = NamedVolumeInfo(
        "thermocycler_executable", "/volumes/thermocycler_volume"
    )


@dataclass(frozen=True)
class OpentronsModulesEmulatorNamedVolumes:
    """Expected named volumes for opentrons-modules emulator containers."""

    HEATER_SHAKER = NamedVolumeInfo("heater_shaker_executable", "/executable")
    THERMOCYCLER = NamedVolumeInfo("thermocycler_executable", "/executable")


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
