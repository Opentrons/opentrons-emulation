"""Enumeration for filter strings and their respective image lookups"""

from __future__ import annotations

from enum import Enum
from typing import List

from .errors import InvalidFilterError
from .images import (
    CANServerImage,
    EmulatorProxyImage,
    FirmwareAndHardwareImages,
    HeaterShakerModuleImages,
    LocalMonorepoBuilderImage,
    LocalOpentronsModulesBuilderImage,
    LocalOT3FirmwareBuilderImage,
    MagneticModuleImages,
    OT3BootloaderImage,
    OT3GantryXImage,
    OT3GantryYImage,
    OT3GripperImage,
    OT3HeadImage,
    OT3PipettesImage,
    OT3StateManagerImage,
    RobotServerImage,
    SingleImage,
    SmoothieImage,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)


class ContainerFilters(Enum):
    """Enumeration of filters and the respective images to look up for them."""

    HEATER_SHAKER_MODULE = ("heater-shaker-module", [HeaterShakerModuleImages()])
    MAGNETIC_MODULE = ("magnetic-module", [MagneticModuleImages()])
    THERMOCYCLER_MODULE = ("thermocycler-module", [ThermocyclerModuleImages()])
    TEMPERATURE_MODULE = ("temperature-module", [TemperatureModuleImages()])
    EMULATOR_PROXY = ("emulator-proxy", [EmulatorProxyImage()])

    SMOOTHIE = ("smoothie", [SmoothieImage()])

    CAN_SERVER = ("can-server", [CANServerImage()])

    OT3_GANTRY_X = ("ot3-gantry-x", [OT3GantryXImage()])
    OT3_GANTRY_Y = ("ot3-gantry-y", [OT3GantryYImage()])
    OT3_HEAD = ("ot3-head", [OT3HeadImage()])
    OT3_PIPETTES = ("ot3-pipettes", [OT3PipettesImage()])
    OT3_BOOTLOADER = ("ot3-bootloader", [OT3BootloaderImage()])
    OT3_GRIPPER = ("ot3-gripper", [OT3GripperImage()])
    OT3_STATE_MANAGER = ("ot3-state-manager", [OT3StateManagerImage()])

    LOCAL_OT3_FIRMWARE_BUILDER = (
        "local-ot3-firmware-builder",
        [LocalOT3FirmwareBuilderImage()],
    )
    LOCAL_MONOREPO_BUILDER = (
        "local-monorepo-builder",
        [LocalMonorepoBuilderImage()],
    )
    LOCAL_OPENTRONS_MODULES_BUILDER = (
        "local-opentrons-modules-builder",
        [LocalOpentronsModulesBuilderImage()],
    )

    MODULES = (
        "modules",
        [
            MagneticModuleImages(),
            ThermocyclerModuleImages(),
            TemperatureModuleImages(),
            HeaterShakerModuleImages(),
        ],
    )
    FIRMWARE = (
        "firmware",
        [
            OT3GantryXImage(),
            OT3GantryYImage(),
            OT3HeadImage(),
            OT3PipettesImage(),
            OT3BootloaderImage(),
            OT3GripperImage(),
            SmoothieImage(),
        ],
    )
    ROBOT_SERVER = ("robot-server", [RobotServerImage()])

    ALL = (
        "all",
        [
            CANServerImage(),
            EmulatorProxyImage(),
            HeaterShakerModuleImages(),
            MagneticModuleImages(),
            OT3GantryXImage(),
            OT3GantryYImage(),
            OT3HeadImage(),
            OT3PipettesImage(),
            OT3BootloaderImage(),
            OT3GripperImage(),
            RobotServerImage(),
            SmoothieImage(),
            TemperatureModuleImages(),
            ThermocyclerModuleImages(),
            OT3StateManagerImage(),
            LocalOT3FirmwareBuilderImage(),
            LocalMonorepoBuilderImage(),
            LocalOpentronsModulesBuilderImage(),
        ],
    )

    def __init__(
        self,
        filter_name: str,
        images: List[FirmwareAndHardwareImages | SingleImage] = [],
    ) -> None:
        self.filter_name = filter_name
        self.images = images

    @classmethod
    def load_by_filter_name(cls, filter_name: str) -> ContainerFilters:
        """Load ContainerFilters object by filter_name"""
        for member in cls.__members__.values():
            if filter_name == member.filter_name:
                return member
        raise InvalidFilterError(
            filter_name, [member.filter_name for member in cls.__members__.values()]
        )
