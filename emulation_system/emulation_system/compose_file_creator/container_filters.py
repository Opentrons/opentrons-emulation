"""Enumeration for filter strings and their respective image lookups"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import List

from . import (
    BuildItem,
    Service,
)
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


@dataclass
class ContainerFilter:
    filter_name: str
    images: List[FirmwareAndHardwareImages | SingleImage]
    firmware_only: bool = False
    hardware_only: bool = False

    def __post_init__(self):
        if self.firmware_only and self.hardware_only:
            raise ValueError(
                'Can not have both "firmware_only" and "hardware_only" set to True'
            )

@dataclass(frozen=True)
class ContainerFilterNames:
        ALL = "all"
        ALL_FIRMWARE_MODULES = "all-firmware-modules"
        ALL_HARDWARE_MODULES = "all-hardware-modules"
        ALL_HEATER_SHAKER_MODULE = "all-heater-shaker-module"
        ALL_MAGNETIC_MODULE = "all-magnetic-module"
        ALL_MODULES = "all-modules"
        ALL_TEMPERATURE_MODULE = "all-temperature-module"
        ALL_THERMOCYCLER_MODULE = "all-thermocycler-module"
        CAN_SERVER = "can-server"
        EMULATOR_PROXY = "emulator-proxy"
        FIRMWARE_HEATER_SHAKER_MODULES = "firmware-heater-shaker-modules"
        FIRMWARE_MAGNETIC_MODULES = "firmware-magnetic-modules"
        FIRMWARE_TEMPERATURE_MODULES = "firmware-temperature-modules"
        FIRMWARE_THERMOCYCLER_MODULES = "firmware-thermocycler-modules"
        HARDWARE_HEATER_SHAKER_MODULES = "hardware-heater-shaker-modules"
        HARDWARE_MAGNETIC_MODULES = "hardware-magnetic-modules"
        HARDWARE_TEMPERATURE_MODULES = "hardware-temperature-modules"
        HARDWARE_THERMOCYCLER_MODULES = "hardware-thermocycler-modules"
        MONOREPO_BUILDER = "monorepo-builder"
        MONOREPO_CONTAINERS = "monorepo-containers"
        OPENTRONS_MODULES_BUILDER = "opentrons-modules-builder"
        OT3_BOOTLOADER = "ot3-bootloader"
        OT3_FIRMWARE = "ot3-firmware"
        OT3_FIRMWARE_BUILDER = "ot3-firmware-builder"
        OT3_GANTRY_X = "ot3-gantry-x"
        OT3_GANTRY_Y = "ot3-gantry-y"
        OT3_GRIPPER = "ot3-gripper"
        OT3_HEAD = "ot3-head"
        OT3_PIPETTES = "ot3-pipettes"
        OT3_STATE_MANAGER = "ot3-state-manager"
        ROBOT_SERVER = "robot-server"
        SMOOTHIE = "smoothie"
        SOURCE_BUILDERS = "source-builders"


@dataclass(frozen=True)
class ContainerFilters:
    """Enumeration of filters and the respective images to look up for them."""

    ALL: ContainerFilter = ContainerFilter(ContainerFilterNames().ALL [CANServerImage(), EmulatorProxyImage(), HeaterShakerModuleImages(), MagneticModuleImages(), OT3GantryXImage(), OT3GantryYImage(), OT3HeadImage(), OT3PipettesImage(), OT3BootloaderImage(), OT3GripperImage(), RobotServerImage(), SmoothieImage(), TemperatureModuleImages(), ThermocyclerModuleImages(), OT3StateManagerImage(), OT3FirmwareBuilderImage(), MonorepoBuilderImage(), OpentronsModulesBuilderImage(),])
    ALL_HEATER_SHAKER_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().ALL_HEATER_SHAKER_MODULES [HeaterShakerModuleImages()])
    ALL_MAGNETIC_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().ALL_MAGNETIC_MODULES [MagneticModuleImages()])
    ALL_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().ALL_MODULES [MagneticModuleImages(), ThermocyclerModuleImages(), TemperatureModuleImages(), HeaterShakerModuleImages()])
    ALL_TEMPERATURE_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().ALL_TEMPERATURE_MODULES [TemperatureModuleImages()])
    ALL_THERMOCYCLER_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().ALL_THERMOCYCLER_MODULES [ThermocyclerModuleImages()])
    CAN_SERVER: ContainerFilter = ContainerFilter(ContainerFilterNames().CAN_SERVER [CANServerImage()])
    CONTAINERS_USING_MONOREPO: ContainerFilter = ContainerFilter(ContainerFilterNames().CONTAINERS_USING_MONOREPO [CANServerImage(), EmulatorProxyImage(), RobotServerImage(), SmoothieImage(), MagneticModuleImages(), ThermocyclerModuleImages(), TemperatureModuleImages(), HeaterShakerModuleImages()], firmware_only=True)
    EMULATOR_PROXY: ContainerFilter = ContainerFilter(ContainerFilterNames().EMULATOR_PROXY [EmulatorProxyImage()])
    FIRMWARE_HEATER_SHAKER_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().FIRMWARE_HEATER_SHAKER_MODULES [HeaterShakerModuleImages()], firmware_only=True)
    FIRMWARE_MAGNETIC_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().FIRMWARE_MAGNETIC_MODULES [MagneticModuleImages()], firmware_only=True)
    FIRMWARE_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().FIRMWARE_MODULES [MagneticModuleImages(), ThermocyclerModuleImages(), TemperatureModuleImages(), HeaterShakerModuleImages()], firmware_only=True)
    FIRMWARE_TEMPERATURE_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().FIRMWARE_TEMPERATURE_MODULES [TemperatureModuleImages()], firmware_only=True)
    FIRMWARE_THERMOCYCLER_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().FIRMWARE_THERMOCYCLER_MODULES [ThermocyclerModuleImages()], firmware_only=True)
    HARDWARE_HEATER_SHAKER_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().HARDWARE_HEATER_SHAKER_MODULES [HeaterShakerModuleImages()], hardware_only=True)
    HARDWARE_MAGNETIC_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().HARDWARE_MAGNETIC_MODULES [MagneticModuleImages()], hardware_only=True)
    HARDWARE_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().HARDWARE_MODULES [MagneticModuleImages(), ThermocyclerModuleImages(), TemperatureModuleImages(), HeaterShakerModuleImages()], hardware_only=True)
    HARDWARE_TEMPERATURE_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().HARDWARE_TEMPERATURE_MODULES [TemperatureModuleImages()], hardware_only=True)
    HARDWARE_THERMOCYCLER_MODULES: ContainerFilter = ContainerFilter(ContainerFilterNames().HARDWARE_THERMOCYCLER_MODULES [ThermocyclerModuleImages()], hardware_only=True)
    MONOREPO_BUILDER: ContainerFilter = ContainerFilter(ContainerFilterNames().MONOREPO_BUILDER [MonorepoBuilderImage()])
    OPENTRONS_MODULES_BUILDER: ContainerFilter = ContainerFilter(ContainerFilterNames().OPENTRONS_MODULES_BUILDER [OpentronsModulesBuilderImage()])
    OT3_BOOTLOADER: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_BOOTLOADER [OT3BootloaderImage()])
    OT3_FIRMWARE: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_FIRMWARE [OT3GantryXImage(), OT3GantryYImage(), OT3HeadImage(), OT3PipettesImage(), OT3BootloaderImage(), OT3GripperImage(), SmoothieImage()])
    OT3_FIRMWARE_BUILDER: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_FIRMWARE_BUILDER [OT3FirmwareBuilderImage()])
    OT3_GANTRY_X: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_GANTRY_X [OT3GantryXImage()])
    OT3_GANTRY_Y: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_GANTRY_Y [OT3GantryYImage()])
    OT3_GRIPPER: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_GRIPPER [OT3GripperImage()])
    OT3_HEAD: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_HEAD [OT3HeadImage()])
    OT3_PIPETTES: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_PIPETTES [OT3PipettesImage()])
    OT3_STATE_MANAGER: ContainerFilter = ContainerFilter(ContainerFilterNames().OT3_STATE_MANAGER [OT3StateManagerImage()])
    ROBOT_SERVER: ContainerFilter = ContainerFilter(ContainerFilterNames().ROBOT_SERVER [RobotServerImage()])
    SMOOTHIE: ContainerFilter = ContainerFilter(ContainerFilterNames().SMOOTHIE [SmoothieImage()])
    SOURCE_BUILDERS: ContainerFilter = ContainerFilter(ContainerFilterNames().SOURCE_BUILDERS [OT3FirmwareBuilderImage(), MonorepoBuilderImage(), OpentronsModulesBuilderImage()])

    def load_by_filter_name(self, filter_name: str) -> ContainerFilter:
        """Load ContainerFilters object by filter_name"""

        for field in fields(self):
            member: ContainerFilter = getattr(self, field.name)
            if filter_name == member.filter_name:
                return member
        raise InvalidFilterError(
            filter_name, [member.filter_name for member in fields(self)]
        )

    def filter_services(
        self, filter_name: str, services: List[Service]
    ) -> List[Service]:

        service_list = []
        image_names = []
        inverse = False

        if filter_name.startswith("not-"):
            inverse = True
            filter_name = filter_name.replace("not-", "")

        container_filter: ContainerFilter = self.load_by_filter_name(filter_name)

        for image in container_filter.images:
            image_names.extend(
                image.get_image_names(
                    only_firmware_level=container_filter.firmware_only,
                    only_hardware_level=container_filter.hardware_only
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
