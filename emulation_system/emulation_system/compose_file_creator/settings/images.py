"""Mapping for getting image names for hardware."""
from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import Literal

from emulation_system.compose_file_creator.errors import ImageNotDefinedError
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    SourceType,
)


class Images(BaseModel):
    """Stores names of images for each piece of hardware."""

    local_firmware_image_name: Optional[str]
    local_hardware_image_name: Optional[str]
    remote_firmware_image_name: Optional[str]
    remote_hardware_image_name: Optional[str]

    def get_image_names(self) -> List[str]:
        """Get list of image names for image."""
        return [
            image_name
            for image_name in [
                self.local_firmware_image_name,
                self.local_hardware_image_name,
                self.remote_firmware_image_name,
                self.remote_hardware_image_name,
            ]
            if image_name is not None
        ]


class HeaterShakerModuleImages(Images):
    """Image names for Heater-Shaker."""

    local_firmware_image_name: Literal[None] = None
    local_hardware_image_name: str = "heater-shaker-hardware-local"
    remote_firmware_image_name: Literal[None] = None
    remote_hardware_image_name: str = "heater-shaker-hardware-remote"


class MagneticModuleImages(Images):
    """Image names for Magnetic Module."""

    local_firmware_image_name: str = "magdeck-firmware-local"
    local_hardware_image_name: Literal[None] = None
    remote_firmware_image_name: str = "magdeck-firmware-remote"
    remote_hardware_image_name: Literal[None] = None


class TemperatureModuleImages(Images):
    """Image names for Temperature Module."""

    local_firmware_image_name: str = "tempdeck-firmware-local"
    local_hardware_image_name: Literal[None] = None
    remote_firmware_image_name: str = "tempdeck-firmware-remote"
    remote_hardware_image_name: Literal[None] = None


class ThermocyclerModuleImages(Images):
    """Image names for Magnetic Module."""

    local_firmware_image_name: str = "thermocycler-firmware-local"
    local_hardware_image_name: str = "thermocycler-hardware-local"
    remote_firmware_image_name: str = "thermocycler-firmware-remote"
    remote_hardware_image_name: str = "thermocycler-hardware-remote"


class RobotServerImages(Images):
    """Image names for Magnetic Module."""

    local_firmware_image_name: str = "robot-server-local"
    local_hardware_image_name: str = "robot-server-local"
    remote_firmware_image_name: str = "robot-server-remote"
    remote_hardware_image_name: str = "robot-server-remote"


class EmulatorProxyImages(Images):
    """Image names for Emulator Proxy."""

    local_firmware_image_name: str = "emulator-proxy-local"
    local_hardware_image_name: Literal[None] = None
    remote_firmware_image_name: str = "emulator-proxy-remote"
    remote_hardware_image_name: Literal[None] = None


class SmoothieImages(Images):
    """Image names for Smoothie."""

    local_firmware_image_name: str = "smoothie-local"
    local_hardware_image_name: Literal[None] = None
    remote_firmware_image_name: str = "smoothie-remote"
    remote_hardware_image_name: Literal[None] = None


class OT3PipettesImages(Images):
    """Image names for OT3 Pipettes."""

    local_firmware_image_name: Literal[None] = None
    local_hardware_image_name: str = "ot3-pipettes-hardware-local"
    remote_firmware_image_name: Literal[None] = None
    remote_hardware_image_name: str = "ot3-pipettes-hardware-remote"


class OT3HeadImages(Images):
    """Image names for OT3 Pipettes."""

    local_firmware_image_name: Literal[None] = None
    local_hardware_image_name: str = "ot3-head-hardware-local"
    remote_firmware_image_name: Literal[None] = None
    remote_hardware_image_name: str = "ot3-head-hardware-remote"


class OT3GantryXImages(Images):
    """Image names for OT3 Pipettes."""

    local_firmware_image_name: Literal[None] = None
    local_hardware_image_name: str = "ot3-gantry-x-hardware-local"
    remote_firmware_image_name: Literal[None] = None
    remote_hardware_image_name: str = "ot3-gantry-x-hardware-remote"


class OT3GantryYImages(Images):
    """Image names for OT3 Pipettes."""

    local_firmware_image_name: Literal[None] = None
    local_hardware_image_name: str = "ot3-gantry-y-hardware-local"
    remote_firmware_image_name: Literal[None] = None
    remote_hardware_image_name: str = "ot3-gantry-y-hardware-remote"


IMAGE_MAPPING = {
    Hardware.HEATER_SHAKER_MODULE.value: HeaterShakerModuleImages(),
    Hardware.MAGNETIC_MODULE.value: MagneticModuleImages(),
    Hardware.THERMOCYCLER_MODULE.value: ThermocyclerModuleImages(),
    Hardware.TEMPERATURE_MODULE.value: TemperatureModuleImages(),
    # TODO: Will need to update OT2 to use Smoothie image once it is created
    Hardware.OT2.value: RobotServerImages(),
    # TODO: Will need to update OT3 to use OT3 image once it is created
    Hardware.OT3.value: RobotServerImages(),
}


def get_image_name(
    hardware: str, source_type: SourceType, emulation_level: EmulationLevels
) -> str:
    """Load image name."""
    image_class = IMAGE_MAPPING[hardware]
    comp_tuple = (source_type, emulation_level)

    if comp_tuple == (SourceType.REMOTE, EmulationLevels.HARDWARE):
        image_name = image_class.remote_hardware_image_name
    elif comp_tuple == (SourceType.REMOTE, EmulationLevels.FIRMWARE):
        image_name = image_class.remote_firmware_image_name
    elif comp_tuple == (SourceType.LOCAL, EmulationLevels.HARDWARE):
        image_name = image_class.local_hardware_image_name
    else:  # (SourceType.LOCAL, EmulationLevels.FIRMWARE)
        image_name = image_class.local_firmware_image_name

    if image_name is None:
        raise ImageNotDefinedError(emulation_level, source_type, hardware)

    return image_name
