"""Module containing logic for e2e tests."""
from dataclasses import dataclass, field
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

    emulator_proxy_name: str
    opentrons_modules_builder_name: str


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

    # def compare(
    #     self,
    #     ot3_system: OT3SystemUnderTest,
    #     modules: ModuleContainerNames,
    #     mounts: ExpectedBindMounts,
    # ) -> None:
    #     """Public facing method to run all above protected assertion methods."""
    #
    #     if self.monorepo_builder_created:
    #         confirm_mount_does_not_exist(ot3_system.monorepo_builder, ENTRYPOINT_MOUNT)
    #
    #     if self.ot3_firmware_builder_created:
    #         confirm_mount_does_not_exist(ot3_system.firmware_builder, ENTRYPOINT_MOUNT)
    #
    #
    #     if self.opentrons_modules_builder_created:
    #         confirm_mount_does_not_exist(ot3_system.modules_builder, ENTRYPOINT_MOUNT)
    #
    #
    #     if (
    #         self.local_monorepo_mounted
    #         and self.monorepo_builder_created
    #         and mounts.MONOREPO is not None
    #     ):
    #
    #         confirm_mount_exists(ot3_system.monorepo_builder, mounts.MONOREPO)
    #
    #     if (
    #         self.local_ot3_firmware_mounted
    #         and self.ot3_firmware_builder_created
    #         and mounts.FIRMWARE is not None
    #     ):
    #         confirm_mount_exists(ot3_system.firmware_builder, mounts.FIRMWARE)
    #
    #     if (
    #         self.local_opentrons_modules_mounted
    #         and self.opentrons_modules_builder_created
    #         and mounts.MODULES is not None
    #     ):
    #
    #         confirm_mount_exists(ot3_system.modules_builder, mounts.MODULES)
