"""Dataclass to easily access all module containers in system."""

from dataclasses import dataclass
from typing import List, Optional

from docker.models.containers import Container  # type: ignore[import]

from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)
from tests.e2e.test_definition.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.helper_functions import get_mounts


@dataclass
class ModuleContainers:
    """Dataclass to access all module containers emulated system easily."""

    hardware_emulation_thermocycler_modules: List[Container]
    firmware_emulation_thermocycler_modules: List[Container]
    hardware_emulation_heater_shaker_modules: List[Container]
    firmware_emulation_heater_shaker_modules: List[Container]
    firmware_emulation_magnetic_modules: List[Container]
    firmware_emulation_temperature_modules: List[Container]

    emulator_proxy: Container
    opentrons_modules_builder: Optional[Container]

    @property
    def no_modules(self) -> bool:
        return (
            self.hardware_emulation_thermocycler_modules == set([]) and
            self.firmware_emulation_thermocycler_modules == set([]) and
            self.hardware_emulation_heater_shaker_modules == set([]) and
            self.firmware_emulation_heater_shaker_modules == set([]) and
            self.firmware_emulation_magnetic_modules == set([]) and
            self.firmware_emulation_temperature_modules == set([])
        )

    @property
    def opentrons_modules_builder_created(self) -> bool:
        """Whether the opentrons-modules builder container was created."""
        return self.opentrons_modules_builder is not None

    @property
    def local_opentrons_modules_mounted(self) -> bool:
        """Whether the opentrons-modules builder container has local source mounted."""
        if self.opentrons_modules_builder is None:
            return False

        modules_builder_mounts = get_mounts(self.opentrons_modules_builder)
        return (
            self.opentrons_modules_builder_created
            and modules_builder_mounts is not None
            and any(
                mount.DEST_PATH == "/opentrons-modules"
                for mount in modules_builder_mounts
            )
        )

    @property
    def opentrons_modules_build_args(self) -> "BuildArgConfigurations":
        """Returns BuildArgConfigurations object representing where source was pulled from."""
        return BuildArgConfigurations.parse_build_args(
            self.opentrons_modules_builder,
            "opentrons-modules/archive/refs/heads/edge.zip",
            RepoToBuildArgMapping.OPENTRONS_MODULES,
        )

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

    @property
    def number_of_modules(self) -> int:
        return len(self.all_modules)
