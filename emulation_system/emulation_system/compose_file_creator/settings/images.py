"""Mapping for getting image names for hardware."""
from typing import Optional

from typing_extensions import Literal

from pydantic import BaseModel

from emulation_system.compose_file_creator.settings.config_file_settings import Hardware


class Images(BaseModel):
    """Stores names of images for each piece of hardware."""

    local_firmware_image_name: Optional[str]
    local_hardware_image_name: Optional[str]
    remote_firmware_image_name: Optional[str]
    remote_hardware_image_name: Optional[str]


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


class OT2Images(Images):
    """Image names for Magnetic Module."""

    local_firmware_image_name: str = "robot-server-local"
    local_hardware_image_name: Literal[None] = None
    remote_firmware_image_name: str = "robot-server-remote"
    remote_hardware_image_name: Literal[None] = None


IMAGE_MAPPING = {
    Hardware.HEATER_SHAKER_MODULE.value: HeaterShakerModuleImages(),
    Hardware.MAGNETIC_MODULE.value: MagneticModuleImages(),
    Hardware.THERMOCYCLER_MODULE.value: ThermocyclerModuleImages(),
    Hardware.TEMPERATURE_MODULE.value: TemperatureModuleImages(),
    Hardware.OT2.value: OT2Images(),
}
