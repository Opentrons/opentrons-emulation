"""Module containing logic for e2e tests."""
from dataclasses import dataclass
from typing import Set

from tests.e2e.test_definition.build_arg_configurations import BuildArgConfigurations


@dataclass
class ModuleConfiguration:
    total_number_of_modules: int
    hw_heater_shaker_module_names: Set[str]
    hw_thermocycler_module_names: Set[str]
    fw_heater_shaker_module_names: Set[str]
    fw_thermocycler_module_names: Set[str]
    fw_magnetic_module_names: Set[str]
    fw_temperature_module_names: Set[str]

    @classmethod
    def NO_MODULES(cls) -> "ModuleConfiguration":
        return cls(
            total_number_of_modules=0,
            hw_heater_shaker_module_names=set([]),
            hw_thermocycler_module_names=set([]),
            fw_heater_shaker_module_names=set([]),
            fw_thermocycler_module_names=set([]),
            fw_magnetic_module_names=set([]),
            fw_temperature_module_names=set([])
        )


    def is_no_modules(self) -> bool:
        return self == self.NO_MODULES()


@dataclass
class SystemTestDefinition:
    """Class representing expected results for a specific yaml configuration file."""

    test_id: str
    yaml_config_relative_path: str

    monorepo_builder_created: bool
    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool

    local_monorepo_mounted: bool
    local_ot3_firmware_mounted: bool
    local_opentrons_modules_mounted: bool

    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations

    module_configuration: ModuleConfiguration
