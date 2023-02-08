from dataclasses import dataclass
from typing import List, Optional

from docker.models.containers import Container


@dataclass
class ModuleContainers:
    """Dataclass to access all module containers emulated system easily."""

    hardware_emulation_thermocycler_modules: Optional[List[Container]]
    firmware_emulation_thermocycler_modules: Optional[List[Container]]
    hardware_emulation_heater_shaker_modules: Optional[List[Container]]
    firmware_emulation_heater_shaker_modules: Optional[List[Container]]
    firmware_emulation_magnetic_modules: Optional[List[Container]]
    firmware_emulation_temperature_modules: Optional[List[Container]]

    @property
    def all_modules(self) -> List[Container]:
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
        return (
            self.firmware_emulation_thermocycler_modules
            + self.firmware_emulation_heater_shaker_modules
            + self.firmware_emulation_magnetic_modules
            + self.firmware_emulation_temperature_modules
        )
