"""Enumeration for filter strings and their respective image lookups"""

from __future__ import annotations

from enum import Enum
from typing import List, Type

from emulation_system.compose_file_creator.errors import InvalidFilterError
from emulation_system.compose_file_creator.settings.images import (
    CANServerImages,
    EmulatorProxyImages,
    HeaterShakerModuleImages,
    Images,
    MagneticModuleImages,
    OT3BootloaderImages,
    OT3GantryXImages,
    OT3GantryYImages,
    OT3GripperImages,
    OT3HeadImages,
    OT3PipettesImages,
    RobotServerImages,
    SmoothieImages,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)


class ContainerFilters(Enum):
    """Enumeration of filters and the respective images to look up for them."""

    HEATER_SHAKER_MODULE = ("heater-shaker-module", [HeaterShakerModuleImages])
    MAGNETIC_MODULE = ("magnetic-module", [MagneticModuleImages])
    THERMOCYCLER_MODULE = ("thermocycler-module", [ThermocyclerModuleImages])
    TEMPERATURE_MODULE = ("temperature-module", [TemperatureModuleImages])
    EMULATOR_PROXY = ("emulator-proxy", [EmulatorProxyImages])

    SMOOTHIE = ("smoothie", [SmoothieImages])

    CAN_SERVER = ("can-server", [CANServerImages])
    OT3_GANTRY_X = ("ot3-gantry-x", [OT3GantryXImages])
    OT3_GANTRY_Y = ("ot3-gantry-y", [OT3GantryYImages])
    OT3_HEAD = ("ot3-head", [OT3HeadImages])
    OT3_PIPETTES = ("ot3-pipettes", [OT3PipettesImages])
    OT3_BOOTLOADER = ("ot3-bootloader", [OT3BootloaderImages])
    OT3_GRIPPER = ("ot3-gripper", [OT3GripperImages])

    MODULES = (
        "modules",
        [
            MagneticModuleImages,
            ThermocyclerModuleImages,
            TemperatureModuleImages,
            HeaterShakerModuleImages,
        ],
    )
    FIRMWARE = (
        "firmware",
        [
            OT3GantryXImages,
            OT3GantryYImages,
            OT3HeadImages,
            OT3PipettesImages,
            OT3BootloaderImages,
            OT3GripperImages,
            SmoothieImages,
        ],
    )
    ROBOT_SERVER = ("robot-server", [RobotServerImages])

    ALL = (
        "all",
        [
            CANServerImages,
            EmulatorProxyImages,
            HeaterShakerModuleImages,
            MagneticModuleImages,
            OT3GantryXImages,
            OT3GantryYImages,
            OT3HeadImages,
            OT3PipettesImages,
            OT3BootloaderImages,
            OT3GripperImages,
            RobotServerImages,
            SmoothieImages,
            TemperatureModuleImages,
            ThermocyclerModuleImages,
        ],
    )

    def __init__(self, filter_name: str, images: List[Type[Images]] = []) -> None:
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
