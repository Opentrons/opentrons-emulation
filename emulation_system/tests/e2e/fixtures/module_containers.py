"""Dataclass to easily access all module containers in system."""

from dataclasses import dataclass
from typing import List, Optional

from docker.models.containers import Container  # type: ignore[import]


@dataclass
class ModuleContainers:
    """Dataclass to access all module containers emulated system easily."""

    hardware_emulation_thermocycler_modules: List[Container]
    firmware_emulation_thermocycler_modules: List[Container]
    hardware_emulation_heater_shaker_modules: List[Container]
    firmware_emulation_heater_shaker_modules: List[Container]
    firmware_emulation_magnetic_modules: List[Container]
    firmware_emulation_temperature_modules: List[Container]

    @property
    def all_modules(self) -> List[Container]:
        """Returns list of all modules in emulated system."""
        return (
            self.hardware_emulation_thermocycler_modules
            + self.hardware_emulation_heater_shaker_modules
            + self.firmware_emulation_thermocycler_modules
            + self.firmware_emulation_heater_shaker_modules
            + self.firmware_emulation_magnetic_modules
            + self.firmware_emulation_temperature_modules
        )

    @property
    def firmware_level_modules(self) -> List[Container]:
        """Returns list of all modules that are using firmware emulation in the emulated system."""
        return (
            self.firmware_emulation_thermocycler_modules
            + self.firmware_emulation_heater_shaker_modules
            + self.firmware_emulation_magnetic_modules
            + self.firmware_emulation_temperature_modules
        )