import os
from dataclasses import dataclass

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
class OT3FirmwareBuilderNamedVolumes:
    GANTRY_X = ExpectedNamedVolume("gantry_x_executable", "/executable")
    GANTRY_Y = ExpectedNamedVolume("gantry_y_executable", "/executable")
    HEAD = ExpectedNamedVolume("head_executable", "/executable")
    GRIPPER = ExpectedNamedVolume("gripper_executable", "/executable")
    PIPETTES = ExpectedNamedVolume("pipettes_executable", "/executable")
    BOOTLOADER = ExpectedNamedVolume("bootloader_executable", "/executable")


@dataclass(frozen=True)
class MonorepoBuilderNamedVolumes:
    MONOREPO_WHEELS = ExpectedNamedVolume("monorepo-wheels", "/dist")


@dataclass(frozen=True)
class CommonMounts:
    ENTRYPOINT_MOUNT = ExpectedMount(
        os.path.join(DOCKERFILE_DIR_LOCATION, "entrypoint.sh"), "/entrypoint.sh"
    )
