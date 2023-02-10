import abc
import os
from dataclasses import dataclass
from typing import Tuple

from emulation_system.consts import DOCKERFILE_DIR_LOCATION


@dataclass(frozen=True)
class ExpectedNamedVolume:
    VOLUME_NAME: str
    DEST_PATH: str


@dataclass(frozen=True)
class ExpectedMount:
    SOURCE_PATH: str
    DEST_PATH: str


@dataclass(frozen=True)
class OT3FirmwareEmulatorNamedVolumesMap:
    GANTRY_X = ExpectedNamedVolume("gantry_x_executable", "/executable")
    GANTRY_Y = ExpectedNamedVolume("gantry_y_executable", "/executable")
    HEAD = ExpectedNamedVolume("head_executable", "/executable")
    GRIPPER = ExpectedNamedVolume("gripper_executable", "/executable")
    PIPETTES = ExpectedNamedVolume("pipettes_executable", "/executable")
    BOOTLOADER = ExpectedNamedVolume("bootloader_executable", "/executable")


@dataclass(frozen=True)
class NamedVolumeList(abc.ABC):
    VOLUMES: Tuple[ExpectedNamedVolume]


@dataclass(frozen=True)
class OT3FirmwareBuilderNamedVolumes(NamedVolumeList):
    VOLUMES: Tuple[ExpectedNamedVolume] = (
        ExpectedNamedVolume("gantry_x_executable", "/volumes/gantry_x_volume"),
        ExpectedNamedVolume("gantry_y_executable", "/volumes/gantry_y_volume"),
        ExpectedNamedVolume("head_executable", "/volumes/head_volume"),
        ExpectedNamedVolume("gripper_executable", "/volumes/gripper_volume"),
        ExpectedNamedVolume("pipettes_executable", "/volumes/pipettes_volume"),
        ExpectedNamedVolume("bootloader_executable", "/volumes/bootloader_volume"),
        ExpectedNamedVolume("state_manager_venv", "/ot3-firmware/build-host/.venv"),
    )


@dataclass(frozen=True)
class CommonNamedVolumes:
    MONOREPO_WHEELS = ExpectedNamedVolume("monorepo-wheels", "/dist")


@dataclass(frozen=True)
class MonorepoBuilderNamedVolumes(NamedVolumeList):
    VOLUMES: Tuple[ExpectedNamedVolume] = (CommonNamedVolumes.MONOREPO_WHEELS,)


@dataclass(frozen=True)
class OpentronsModulesBuilderNamedVolumes(NamedVolumeList):
    VOLUMES: Tuple[ExpectedNamedVolume] = (
        ExpectedNamedVolume(
            "heater_shaker_executable", "/volumes/heater_shaker_volume"
        ),
        ExpectedNamedVolume("thermocycler_executable", "/volumes/thermocycler_volume"),
    )


@dataclass(frozen=True)
class OpentronsModulesEmulatorNamedVolumes:
    HEATER_SHAKER = ExpectedNamedVolume("heater_shaker_executable", "/executable")
    THERMOCYCLER = ExpectedNamedVolume("thermocycler_executable", "/executable")


@dataclass(frozen=True)
class CommonMounts:
    ENTRYPOINT_MOUNT = ExpectedMount(
        os.path.join(DOCKERFILE_DIR_LOCATION, "entrypoint.sh"), "/entrypoint.sh"
    )


@dataclass(frozen=True)
class OT3StateManagerNamedVolumes:
    VOLUMES: Tuple[ExpectedNamedVolume] = (
        CommonNamedVolumes.MONOREPO_WHEELS,
        ExpectedNamedVolume("state_manager_venv", "/.venv"),
    )


@dataclass(frozen=True)
class OT3FirmwareExpectedBinaryNames:
    GANTRY_X = "gantry-x-simulator"
    GANTRY_Y = "gantry-y-simulator"
    HEAD = "head-simulator"
    GRIPPER = "gripper-simulator"
    PIPETTES = "pipettes-simulator"
    BOOTLOADER = "bootloader-simulator"


@dataclass(frozen=True)
class ModulesExpectedBinaryNames:
    THERMOCYCLER = "thermocycler-simulator"
    HEATER_SHAKER = "heater-shaker-simulator"
