"""ServiceInfo Class."""

from dataclasses import dataclass

from emulation_system.compose_file_creator.config_file_settings import OT3Hardware
from emulation_system.compose_file_creator.images import (
    FirmwareAndHardwareImages,
    OT3BootloaderImage,
    OT3GantryXImage,
    OT3GantryYImage,
    OT3GripperImage,
    OT3HeadImage,
    OT3PipettesImage,
    SingleImage,
)


@dataclass
class ServiceInfo:
    """Info about service to be created."""

    image: FirmwareAndHardwareImages | SingleImage
    ot3_hardware: OT3Hardware

    def is_head(self) -> bool:
        """Whether the service is a head service."""
        return isinstance(self.image, OT3HeadImage)

    def is_gantry_x(self) -> bool:
        """Whether the service is a gantry x service."""
        return isinstance(self.image, OT3GantryXImage)

    def is_gantry_y(self) -> bool:
        """Whether the service is a gantry y service."""
        return isinstance(self.image, OT3GantryYImage)

    def is_pipette(self) -> bool:
        """Whether the service is a pipette service."""
        return isinstance(self.image, OT3PipettesImage)

    def is_gripper(self) -> bool:
        """Whether the service is a gripper service."""
        return isinstance(self.image, OT3GripperImage)

    def is_bootloader(self) -> bool:
        """Whether the service is a bootloader service."""
        return isinstance(self.image, OT3BootloaderImage)

    def is_left_pipette(self) -> bool:
        """Whether the service is a left pipette service."""
        return self.ot3_hardware == OT3Hardware.LEFT_PIPETTE and self.is_pipette()

    def is_right_pipette(self) -> bool:
        """Whether the service is a left pipette service."""
        return self.ot3_hardware == OT3Hardware.RIGHT_PIPETTE and self.is_pipette()
