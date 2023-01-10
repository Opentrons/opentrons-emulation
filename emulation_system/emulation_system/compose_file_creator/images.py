"""Mapping for getting image names for hardware."""
from dataclasses import dataclass
from typing import Dict, List, Optional

from typing_extensions import Literal

from .config_file_settings import EmulationLevels, Hardware
from .errors import ImageNotDefinedError


@dataclass
class FirmwareAndHardwareImages:
    """Represents images that have a hardware and firmware version."""

    firmware_image_name: Optional[str]
    hardware_image_name: Optional[str]

    def get_image_names(self) -> List[str]:
        """Get list of image names for image."""
        return [
            image_name
            for image_name in [self.firmware_image_name, self.hardware_image_name]
            if image_name is not None
        ]


@dataclass
class SingleImage:
    """Represents images that only have a single version."""

    image_name: str

    def get_image_names(self) -> List[str]:
        """Get list of image names for image."""
        return [self.image_name]


@dataclass
class HeaterShakerModuleImages(FirmwareAndHardwareImages):
    """Image names for Heater-Shaker."""

    firmware_image_name: str = "heater-shaker-firmware"
    hardware_image_name: str = "heater-shaker-hardware"


@dataclass
class MagneticModuleImages(FirmwareAndHardwareImages):
    """Image names for Magnetic Module."""

    firmware_image_name: str = "magdeck-firmware"
    hardware_image_name: Literal[None] = None


@dataclass
class TemperatureModuleImages(FirmwareAndHardwareImages):
    """Image names for Temperature Module."""

    firmware_image_name: str = "tempdeck-firmware"
    hardware_image_name: Literal[None] = None


@dataclass
class ThermocyclerModuleImages(FirmwareAndHardwareImages):
    """Image names for Magnetic Module."""

    firmware_image_name: str = "thermocycler-firmware"
    hardware_image_name: str = "thermocycler-hardware"


@dataclass
class RobotServerImage(SingleImage):
    """Image name for Robot Server."""

    image_name: str = "robot-server"


@dataclass
class EmulatorProxyImage(SingleImage):
    """Image name for Emulator Proxy."""

    image_name: str = "emulator-proxy"


@dataclass
class SmoothieImage(SingleImage):
    """Image names for Smoothie."""

    image_name: str = "smoothie"


@dataclass
class OT3PipettesImage(SingleImage):
    """Image names for OT3 Pipettes."""

    image_name: str = "ot3-pipettes-hardware"


@dataclass
class OT3HeadImage(SingleImage):
    """Image names for OT3 Pipettes."""

    image_name: str = "ot3-head-hardware"


@dataclass
class OT3GantryXImage(SingleImage):
    """Image names for OT3 Pipettes."""

    image_name: str = "ot3-gantry-x-hardware"


@dataclass
class OT3GantryYImage(SingleImage):
    """Image names for OT3 Pipettes."""

    image_name: str = "ot3-gantry-y-hardware"


@dataclass
class OT3BootloaderImage(SingleImage):
    """Image names for OT3 Bootloader."""

    image_name: str = "ot3-bootloader-hardware"


@dataclass
class OT3GripperImage(SingleImage):
    """Image names for OT3 Bootloader."""

    image_name: str = "ot3-gripper-hardware"


@dataclass
class OT3StateManagerImage(SingleImage):
    """Image names for OT3 Bootloader."""

    image_name: str = "ot3-state-manager"


@dataclass
class LocalOT3FirmwareBuilderImage(SingleImage):
    """Image names for OT3 Bootloader."""

    image_name: str = "local-ot3-firmware-builder"


@dataclass
class LocalMonorepoBuilderImage(SingleImage):
    """Image names for OT3 Bootloader."""

    image_name: str = "local-monorepo-builder"


@dataclass
class LocalOpentronsModulesBuilderImage(SingleImage):
    """Image names for OT3 Bootloader."""

    image_name: str = "local-opentrons-modules-builder"


@dataclass
class CANServerImage(SingleImage):
    """Image names for CAN server."""

    image_name: str = "can-server"


IMAGE_MAPPING: Dict[str, FirmwareAndHardwareImages | SingleImage] = {
    Hardware.HEATER_SHAKER_MODULE.value: HeaterShakerModuleImages(),
    Hardware.MAGNETIC_MODULE.value: MagneticModuleImages(),
    Hardware.THERMOCYCLER_MODULE.value: ThermocyclerModuleImages(),
    Hardware.TEMPERATURE_MODULE.value: TemperatureModuleImages(),
    Hardware.OT2.value: RobotServerImage(),
    Hardware.OT3.value: RobotServerImage(),
}


def get_image_name(hardware: str, emulation_level: EmulationLevels) -> str:
    """Load image name."""
    image_class: FirmwareAndHardwareImages | SingleImage = IMAGE_MAPPING[hardware]
    image_name: str | None
    if issubclass(image_class.__class__, SingleImage):
        image_name = image_class.image_name
    else:
        if emulation_level == EmulationLevels.HARDWARE:
            image_name = image_class.hardware_image_name
        else:
            image_name = image_class.firmware_image_name

    if image_name is None:
        raise ImageNotDefinedError(emulation_level, hardware)

    return image_name
