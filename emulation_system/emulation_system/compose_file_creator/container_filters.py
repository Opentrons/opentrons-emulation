"""Enumeration for filter strings and their respective image lookups."""

from __future__ import annotations

from enum import Enum, auto, unique
from typing import List

from . import BuildItem, Service
from .errors import InvalidFilterError
from .images import (
    CANServerImage,
    EmulatorProxyImage,
    FirmwareAndHardwareImages,
    HeaterShakerModuleImages,
    MagneticModuleImages,
    MonorepoBuilderImage,
    OpentronsModulesBuilderImage,
    OT3BootloaderImage,
    OT3FirmwareBuilderImage,
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


@unique
class EmulationLevelFilter(Enum):
    """Enum to provide context to different emulation level filters."""

    FIRMWARE_ONLY = auto()
    HARDWARE_ONLY = auto()
    ALL = auto()


@unique
class ContainerFilters(Enum):
    """Enumeration of filters and the respective images to look up for them."""

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
            OT3FirmwareBuilderImage(),
            MonorepoBuilderImage(),
            OpentronsModulesBuilderImage(),
        ],
        EmulationLevelFilter.ALL,
    )
    CAN_SERVER = ("can-server", [CANServerImage()], EmulationLevelFilter.ALL)
    EMULATOR_PROXY = (
        "emulator-proxy",
        [EmulatorProxyImage()],
        EmulationLevelFilter.ALL,
    )
    FIRMWARE_HEATER_SHAKER_MODULES = (
        "firmware-heater-shaker-modules",
        [HeaterShakerModuleImages()],
        EmulationLevelFilter.FIRMWARE_ONLY,
    )
    FIRMWARE_MAGNETIC_MODULES = (
        "firmware-magnetic-modules",
        [MagneticModuleImages()],
        EmulationLevelFilter.FIRMWARE_ONLY,
    )
    FIRMWARE_MODULES = (
        "firmware-modules",
        [
            MagneticModuleImages(),
            ThermocyclerModuleImages(),
            TemperatureModuleImages(),
            HeaterShakerModuleImages(),
        ],
        EmulationLevelFilter.FIRMWARE_ONLY,
    )
    FIRMWARE_TEMPERATURE_MODULES = (
        "firmware-temperature-modules",
        [TemperatureModuleImages()],
        EmulationLevelFilter.FIRMWARE_ONLY,
    )
    FIRMWARE_THERMOCYCLER_MODULES = (
        "firmware-thermocycler-modules",
        [ThermocyclerModuleImages()],
        EmulationLevelFilter.FIRMWARE_ONLY,
    )
    HARDWARE_HEATER_SHAKER_MODULES = (
        "hardware-heater-shaker-modules",
        [HeaterShakerModuleImages()],
        EmulationLevelFilter.HARDWARE_ONLY,
    )
    HARDWARE_MAGNETIC_MODULES = (
        "hardware-magnetic-modules",
        [MagneticModuleImages()],
        EmulationLevelFilter.HARDWARE_ONLY,
    )
    HARDWARE_MODULES = (
        "hardware-modules",
        [
            MagneticModuleImages(),
            ThermocyclerModuleImages(),
            TemperatureModuleImages(),
            HeaterShakerModuleImages(),
        ],
        EmulationLevelFilter.HARDWARE_ONLY,
    )
    HARDWARE_TEMPERATURE_MODULES = (
        "hardware-temperature-modules",
        [TemperatureModuleImages()],
        EmulationLevelFilter.HARDWARE_ONLY,
    )
    HARDWARE_THERMOCYCLER_MODULES = (
        "hardware-thermocycler-modules",
        [ThermocyclerModuleImages()],
        EmulationLevelFilter.HARDWARE_ONLY,
    )
    HEATER_SHAKER_MODULES = (
        "heater-shaker-modules",
        [HeaterShakerModuleImages()],
        EmulationLevelFilter.ALL,
    )
    MAGNETIC_MODULES = (
        "magnetic-modules",
        [MagneticModuleImages()],
        EmulationLevelFilter.ALL,
    )
    MODULES = (
        "modules",
        [
            MagneticModuleImages(),
            ThermocyclerModuleImages(),
            TemperatureModuleImages(),
            HeaterShakerModuleImages(),
        ],
        EmulationLevelFilter.ALL,
    )
    MONOREPO_BUILDER = (
        "monorepo-builder",
        [MonorepoBuilderImage()],
        EmulationLevelFilter.ALL,
    )
    MONOREPO_CONTAINERS = (
        "monorepo-containers",
        [
            CANServerImage(),
            EmulatorProxyImage(),
            RobotServerImage(),
            SmoothieImage(),
            MagneticModuleImages(),
            ThermocyclerModuleImages(),
            TemperatureModuleImages(),
            HeaterShakerModuleImages(),
        ],
        EmulationLevelFilter.FIRMWARE_ONLY,
    )
    OPENTRONS_MODULES_BUILDER = (
        "opentrons-modules-builder",
        [OpentronsModulesBuilderImage()],
        EmulationLevelFilter.ALL,
    )
    OT3_BOOTLOADER = (
        "ot3-bootloader",
        [OT3BootloaderImage()],
        EmulationLevelFilter.ALL,
    )
    OT3_FIRMWARE = (
        "ot3-firmware",
        [
            OT3GantryXImage(),
            OT3GantryYImage(),
            OT3HeadImage(),
            OT3PipettesImage(),
            OT3BootloaderImage(),
            OT3GripperImage(),
            SmoothieImage(),
        ],
        EmulationLevelFilter.ALL,
    )
    OT3_FIRMWARE_BUILDER = (
        "ot3-firmware-builder",
        [OT3FirmwareBuilderImage()],
        EmulationLevelFilter.ALL,
    )
    OT3_GANTRY_X = ("ot3-gantry-x", [OT3GantryXImage()], EmulationLevelFilter.ALL)
    OT3_GANTRY_Y = ("ot3-gantry-y", [OT3GantryYImage()], EmulationLevelFilter.ALL)
    OT3_GRIPPER = ("ot3-gripper", [OT3GripperImage()], EmulationLevelFilter.ALL)
    OT3_HEAD = ("ot3-head", [OT3HeadImage()], EmulationLevelFilter.ALL)
    OT3_PIPETTES = ("ot3-pipettes", [OT3PipettesImage()], EmulationLevelFilter.ALL)
    OT3_STATE_MANAGER = (
        "ot3-state-manager",
        [OT3StateManagerImage()],
        EmulationLevelFilter.ALL,
    )
    ROBOT_SERVER = ("robot-server", [RobotServerImage()], EmulationLevelFilter.ALL)
    SMOOTHIE = ("smoothie", [SmoothieImage()], EmulationLevelFilter.ALL)
    SOURCE_BUILDERS = (
        "source-builders",
        [
            OT3FirmwareBuilderImage(),
            MonorepoBuilderImage(),
            OpentronsModulesBuilderImage(),
        ],
        EmulationLevelFilter.ALL,
    )
    TEMPERATURE_MODULES = (
        "temperature-modules",
        [TemperatureModuleImages()],
        EmulationLevelFilter.ALL,
    )
    THERMOCYCLER_MODULES = (
        "thermocycler-modules",
        [ThermocyclerModuleImages()],
        EmulationLevelFilter.ALL,
    )

    def __init__(
        self,
        container_filter_name: str,
        images: List[FirmwareAndHardwareImages | SingleImage],
        emulation_level_filter: EmulationLevelFilter,
    ) -> None:
        """Constructor to build a container filter.

        Takes name of filter, images that should be returned in the filter,
        and emulation level filter.
        """
        self.container_filter_name = container_filter_name
        self.images = images
        self.emulation_level_filter = emulation_level_filter

    @classmethod
    def _load_by_filter_name(cls, filter_name: str) -> ContainerFilters:
        """Load ContainerFilters object by filter_name."""
        valid_filters = []
        for name, value in cls.__members__.items():
            if filter_name == value.container_filter_name:
                return value
            else:
                valid_filters.append(value.container_filter_name)

        raise InvalidFilterError(filter_name, valid_filters)

    @classmethod
    def filter_services(
        cls, filter_name: str, services: List[Service]
    ) -> List[Service]:
        """Using passed filter name, filter passed list of services.

        Can prefix filter with "not-" to return the inverse of the filters.

        For instance, "not-source-builders" would return all containers that
        are not in the "source-builders" filter.
        """
        service_list = []
        image_names = []
        inverse = False

        if filter_name.startswith("not-"):
            inverse = True
            filter_name = filter_name.replace("not-", "")

        container_filter: ContainerFilters = cls._load_by_filter_name(filter_name)

        for image in container_filter.images:
            firmware_level: bool
            hardware_level: bool
            match container_filter.emulation_level_filter:
                case EmulationLevelFilter.FIRMWARE_ONLY:
                    firmware_level = True
                    hardware_level = False
                case EmulationLevelFilter.HARDWARE_ONLY:
                    firmware_level = False
                    hardware_level = True
                case _:
                    firmware_level = True
                    hardware_level = True

            image_names.extend(
                image.get_image_names(
                    only_firmware_level=firmware_level,
                    only_hardware_level=hardware_level,
                )
            )

        for service in services:
            service_build = service.build
            assert isinstance(service_build, BuildItem)
            if not inverse:
                if service_build.target in image_names:
                    service_list.append(service)
            else:
                if service_build.target not in image_names:
                    service_list.append(service)

        return service_list
