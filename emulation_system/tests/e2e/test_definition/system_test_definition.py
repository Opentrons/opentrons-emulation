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

    # def _confirm_entrypoint_mounts(
    #     self, ot3_system: OT3SystemUnderTest, modules: ModuleContainerNames
    # ) -> None:
    #     containers = ot3_system.containers_with_entrypoint_script + modules.all_modules
    #     for container in containers:
    #         expected_mount = ENTRYPOINT_MOUNT
    #         confirm_mount_exists(container, ENTRYPOINT_MOUNT)

    # def _confirm_containers_with_monorepo_wheel_volumes(
    #     self, ot3_system: OT3SystemUnderTest, modules: ModuleContainerNames
    # ) -> None:
    #     containers = (
    #         ot3_system.containers_with_monorepo_wheel_volume
    #         + modules.firmware_level_modules
    #     )
    #     for container in containers:
    #         for expected_volume in MonorepoBuilderNamedVolumes.VOLUMES:
    #                 confirm_named_volume_exists(container, expected_volume),
    #                 test_description
    #
    # def _confirm_opentrons_modules_builder_named_volumes(
    #     self, ot3_system: OT3SystemUnderTest
    # ) -> None:
    #     for volume in OpentronsModulesBuilderNamedVolumes.VOLUMES:
    #         confirm_named_volume_exists(ot3_system.modules_builder, volume)
    #
    # def _confirm_opentrons_modules_emulator_named_volumes(
    #     self, modules: ModuleContainerNames
    # ) -> None:
    #     heater_shaker_hardware_volume = (
    #         OpentronsModulesEmulatorNamedVolumes.HEATER_SHAKER
    #     )
    #     thermocycler_hardware_volume = OpentronsModulesEmulatorNamedVolumes.THERMOCYCLER
    #     if len(modules.hardware_emulation_heater_shaker_modules) > 0:
    #         for heater_shaker in modules.hardware_emulation_heater_shaker_modules:
    #             confirm_named_volume_exists(
    #                 heater_shaker, heater_shaker_hardware_volume
    #             )
    #
    #     if len(modules.hardware_emulation_thermocycler_modules) > 0:
    #         for thermocycler in modules.hardware_emulation_thermocycler_modules:
    #             confirm_named_volume_exists(thermocycler, thermocycler_hardware_volume)
    #
    # def _confirm_ot3_firmware_build_artifacts(
    #     self, ot3_system: OT3SystemUnderTest
    # ) -> None:
    #     test_matrix = (
    #         (ot3_system.gantry_x, OT3FirmwareExpectedBinaryNames.GANTRY_X),
    #         (ot3_system.gantry_y, OT3FirmwareExpectedBinaryNames.GANTRY_Y),
    #         (ot3_system.head, OT3FirmwareExpectedBinaryNames.HEAD),
    #         (ot3_system.gripper, OT3FirmwareExpectedBinaryNames.GRIPPER),
    #         (ot3_system.pipettes, OT3FirmwareExpectedBinaryNames.PIPETTES),
    #         (ot3_system.bootloader, OT3FirmwareExpectedBinaryNames.BOOTLOADER),
    #     )
    #     for container, expected_sim_name in test_matrix:
    #         assert exec_in_container(container, "ls /executable") == expected_sim_name
    #
    # def _confirm_opentrons_modules_build_artifacts(
    #     self, modules: ModuleContainerNames
    # ) -> None:
    #     test_matrix = (
    #         (
    #             modules.hardware_emulation_thermocycler_modules,
    #             ModulesExpectedBinaryNames.THERMOCYCLER,
    #         ),
    #         (
    #             modules.hardware_emulation_heater_shaker_modules,
    #             ModulesExpectedBinaryNames.HEATER_SHAKER,
    #         ),
    #     )
    #     for container_list, expected_sim_name in test_matrix:
    #         if len(container_list) > 0:
    #             for container in container_list:
    #                 assert (
    #                     exec_in_container(container, "ls /executable")
    #                     == expected_sim_name
    #                 )
    #
    # def compare(
    #     self,
    #     ot3_system: OT3SystemUnderTest,
    #     modules: ModuleContainerNames,
    #     mounts: ExpectedBindMounts,
    # ) -> None:
    #     """Public facing method to run all above protected assertion methods."""
    #     self._confirm_entrypoint_mounts(ot3_system, modules)
    #
    #     if self.monorepo_builder_created:
    #         confirm_mount_does_not_exist(ot3_system.monorepo_builder, ENTRYPOINT_MOUNT)
    #
    #     if self.ot3_firmware_builder_created:
    #         confirm_mount_does_not_exist(ot3_system.firmware_builder, ENTRYPOINT_MOUNT)
    #
    #         self._confirm_ot3_firmware_build_artifacts(ot3_system)
    #
    #     if self.opentrons_modules_builder_created:
    #         confirm_mount_does_not_exist(ot3_system.modules_builder, ENTRYPOINT_MOUNT)
    #         self._confirm_opentrons_modules_builder_named_volumes(ot3_system)
    #         self._confirm_opentrons_modules_emulator_named_volumes(modules)
    #         self._confirm_opentrons_modules_build_artifacts(modules)
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
