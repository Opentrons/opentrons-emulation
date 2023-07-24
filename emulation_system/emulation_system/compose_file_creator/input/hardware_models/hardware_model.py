"""Parent class for all hardware."""
from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    SourceRepositories,
)
from emulation_system.compose_file_creator.images import get_image_name
from opentrons_pydantic_base_model import OpentronsBaseModel

from .hardware_specific_attributes import HardwareSpecificAttributes


class HardwareModel(OpentronsBaseModel):
    """Parent class of all hardware. Define attributes common to all hardware."""

    id: str = Field(..., regex=r"^[a-zA-Z0-9-_]+$")
    hardware: str
    source_repos: SourceRepositories = NotImplemented
    emulation_level: EmulationLevels = NotImplemented
    hardware_specific_attributes: HardwareSpecificAttributes = NotImplemented

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        super().__init__(**data)

    def get_image_name(self) -> str:
        """Get image name to run based off of passed parameters."""
        return get_image_name(self.hardware, self.emulation_level)

    def get_hardware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for module when it is being emulated at hardware level."""
        return None

    def get_firmware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for module when it is being emulated at hardware level."""
        return None

    def is_firmware_emulation_level(self) -> bool:
        """Whether or not module is firmware emulation level."""
        return self.emulation_level == EmulationLevels.FIRMWARE

    def is_hardware_emulation_level(self) -> bool:
        """Whether or not module is hardware emulation level."""
        return self.emulation_level == EmulationLevels.HARDWARE
