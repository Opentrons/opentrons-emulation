"""Dataaclass to easily access all module containers in system."""

from dataclasses import dataclass
from typing import List, Optional

from docker.models.containers import Container  # type: ignore[import]


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
        """Returns list of all modules in emulated system."""
        result_list = []

        for mod_list in [
            self.hardware_emulation_thermocycler_modules,
            self.hardware_emulation_heater_shaker_modules,
            self.firmware_emulation_thermocycler_modules,
            self.firmware_emulation_heater_shaker_modules,
            self.firmware_emulation_magnetic_modules,
            self.firmware_emulation_temperature_modules,
        ]:
            if mod_list is not None:
                result_list.extend(mod_list)

        return result_list

    @property
    def firmware_level_modules(self) -> List[Container]:
        """Returns list of all modules that are using firmware emulation in the emulated system."""
        result_list = []

        for mod_list in [
            self.firmware_emulation_thermocycler_modules,
            self.firmware_emulation_heater_shaker_modules,
            self.firmware_emulation_magnetic_modules,
            self.firmware_emulation_temperature_modules,
        ]:
            if mod_list is not None:
                result_list.extend(mod_list)

        return result_list
