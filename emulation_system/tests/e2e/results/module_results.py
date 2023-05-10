"""Classes extending ModuleResultABC representing expected and actual results of module containers."""

from dataclasses import dataclass
from typing import Dict, List, Set, Type

from docker.models.containers import Container  # type: ignore[import]

from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from e2e.consts import (
    ENTRYPOINT_MOUNT,
    OPENTRONS_MODULES_BUILDER_NAMED_VOLUMES,
    BindMountInfo,
    ModulesExpectedBinaryNames,
    NamedVolumeInfo,
    OpentronsModulesEmulatorNamedVolumes,
)
from e2e.helper_functions import (
    exec_in_container,
    get_container_names,
    get_mounts,
    get_volumes,
)
from e2e.results.results_abc import ModuleResultABC


@dataclass
class ModuleContainerNames(ModuleResultABC):
    """Results to check module names with.

    Because there can be multiple of a module just checking for existence
    is not enough. Need to check that the correct modules were created with
    the correct names.
    Because Docker requires all container names to be unique, names can be used
    as a definitive way to confirm that the correct number of modules were created.
    While we are not directly introspecting into the module and checking all their values for this
    test, it is a good smoke test.
    """

    hw_heater_shaker_module_names: Set[str]
    fw_heater_shaker_module_names: Set[str]
    hw_thermocycler_module_names: Set[str]
    fw_thermocycler_module_names: Set[str]
    fw_magnetic_module_names: Set[str]
    fw_temperature_module_names: Set[str]

    @classmethod
    def NO_MODULES_EXPECTED_RESULT(cls) -> "ModuleContainerNames":
        """If there are no modules all fields should be empty sets."""
        return cls(
            hw_heater_shaker_module_names=set([]),
            fw_heater_shaker_module_names=set([]),
            hw_thermocycler_module_names=set([]),
            fw_thermocycler_module_names=set([]),
            fw_magnetic_module_names=set([]),
            fw_temperature_module_names=set([]),
        )

    @classmethod
    def get_actual_results(
        cls: Type["ModuleContainerNames"], system_under_test: E2EHostSystem
    ) -> "ModuleContainerNames":
        """Get all names of modules from host docker system.

        For each field we want to load a set of the container names from the
        system under test. Using a set because it doesn't matter what order the
        names are in.
        """
        return cls(
            hw_heater_shaker_module_names=get_container_names(
                system_under_test.module_containers.hardware_emulation_heater_shaker_modules
            ),
            fw_heater_shaker_module_names=get_container_names(
                system_under_test.module_containers.firmware_emulation_heater_shaker_modules
            ),
            hw_thermocycler_module_names=get_container_names(
                system_under_test.module_containers.hardware_emulation_thermocycler_modules
            ),
            fw_thermocycler_module_names=get_container_names(
                system_under_test.module_containers.firmware_emulation_thermocycler_modules
            ),
            fw_magnetic_module_names=get_container_names(
                system_under_test.module_containers.firmware_emulation_magnetic_modules
            ),
            fw_temperature_module_names=get_container_names(
                system_under_test.module_containers.firmware_emulation_temperature_modules
            ),
        )

    @classmethod
    def get_expected_results(
        cls: Type["ModuleContainerNames"], system_test_def: SystemTestDefinition
    ) -> "ModuleContainerNames":
        """Get expected module names.

        Loaded directly from SystemTestDefinition object.
        """
        return cls(
            hw_heater_shaker_module_names=system_test_def.module_configuration.hw_heater_shaker_module_names,
            fw_heater_shaker_module_names=system_test_def.module_configuration.fw_heater_shaker_module_names,
            hw_thermocycler_module_names=system_test_def.module_configuration.hw_thermocycler_module_names,
            fw_thermocycler_module_names=system_test_def.module_configuration.fw_thermocycler_module_names,
            fw_magnetic_module_names=system_test_def.module_configuration.fw_magnetic_module_names,
            fw_temperature_module_names=system_test_def.module_configuration.fw_temperature_module_names,
        )


@dataclass
class ModuleNamedVolumes(ModuleResultABC):
    """Checking that each of the module's volumes are correct.

    For each type of module (emulation level and module model), create a dictionary where
    the keys are names of each of the modules, the values are a set containing NamedVolumeInfo objects.
    """

    hw_heater_shaker_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    fw_heater_shaker_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    hw_thermocycler_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    fw_thermocycler_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    fw_magnetic_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    fw_temperature_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]

    @classmethod
    def NO_MODULES_EXPECTED_RESULT(cls) -> "ModuleNamedVolumes":
        """If there are no modules all fields should be empty dictionaries."""
        return cls({}, {}, {}, {}, {}, {})

    @classmethod
    def _generate_heater_shaker_hw_expected_named_volume_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, Set[NamedVolumeInfo]]:
        return {
            container_name: {OpentronsModulesEmulatorNamedVolumes.HEATER_SHAKER}
            for container_name in container_names
        }

    @classmethod
    def _generate_thermocycler_hw_expected_named_volume_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, Set[NamedVolumeInfo]]:
        return {
            container_name: {OpentronsModulesEmulatorNamedVolumes.THERMOCYCLER}
            for container_name in container_names
        }

    @classmethod
    def _generate_fw_expected_named_volume_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, Set[NamedVolumeInfo]]:
        return {
            container_name: {
                NamedVolumeInfo(VOLUME_NAME="monorepo-wheels", DEST_PATH="/dist")
            }
            for container_name in container_names
        }

    @classmethod
    def _get_actual_named_volumes_dict(
        cls, containers: List[Container]
    ) -> Dict[str, Set[NamedVolumeInfo]]:
        return {container.name: set(get_volumes(container)) for container in containers}

    @classmethod
    def get_actual_results(
        cls: Type["ModuleNamedVolumes"], system_under_test: E2EHostSystem
    ) -> "ModuleNamedVolumes":
        """Load volume names for all containers from system under test."""
        return cls(
            hw_heater_shaker_module_named_volumes=cls._get_actual_named_volumes_dict(
                system_under_test.module_containers.hardware_emulation_heater_shaker_modules
            ),
            fw_heater_shaker_module_named_volumes=cls._get_actual_named_volumes_dict(
                system_under_test.module_containers.firmware_emulation_heater_shaker_modules
            ),
            hw_thermocycler_module_named_volumes=cls._get_actual_named_volumes_dict(
                system_under_test.module_containers.hardware_emulation_thermocycler_modules
            ),
            fw_thermocycler_module_named_volumes=cls._get_actual_named_volumes_dict(
                system_under_test.module_containers.firmware_emulation_thermocycler_modules
            ),
            fw_magnetic_module_named_volumes=cls._get_actual_named_volumes_dict(
                system_under_test.module_containers.firmware_emulation_magnetic_modules
            ),
            fw_temperature_module_named_volumes=cls._get_actual_named_volumes_dict(
                system_under_test.module_containers.firmware_emulation_temperature_modules
            ),
        )

    @classmethod
    def get_expected_results(
        cls: Type["ModuleNamedVolumes"], system_test_def: SystemTestDefinition
    ) -> "ModuleNamedVolumes":
        """Get expected results for module volume names."""
        return cls(
            hw_heater_shaker_module_named_volumes=cls._generate_heater_shaker_hw_expected_named_volume_dict(
                system_test_def.module_configuration.hw_heater_shaker_module_names
            ),
            fw_heater_shaker_module_named_volumes=cls._generate_fw_expected_named_volume_dict(
                system_test_def.module_configuration.fw_heater_shaker_module_names
            ),
            hw_thermocycler_module_named_volumes=cls._generate_thermocycler_hw_expected_named_volume_dict(
                system_test_def.module_configuration.hw_thermocycler_module_names
            ),
            fw_thermocycler_module_named_volumes=cls._generate_fw_expected_named_volume_dict(
                system_test_def.module_configuration.fw_thermocycler_module_names
            ),
            fw_magnetic_module_named_volumes=cls._generate_fw_expected_named_volume_dict(
                system_test_def.module_configuration.fw_magnetic_module_names
            ),
            fw_temperature_module_named_volumes=cls._generate_fw_expected_named_volume_dict(
                system_test_def.module_configuration.fw_temperature_module_names
            ),
        )


@dataclass
class ModuleMounts(ModuleResultABC):
    """Ensures that all module containers have entrypoint.sh bound into them."""

    hw_heater_shaker_module_mounts: Dict[str, Set[BindMountInfo]]
    fw_heater_shaker_module_mounts: Dict[str, Set[BindMountInfo]]
    hw_thermocycler_module_mounts: Dict[str, Set[BindMountInfo]]
    fw_thermocycler_module_mounts: Dict[str, Set[BindMountInfo]]
    fw_magnetic_module_mounts: Dict[str, Set[BindMountInfo]]
    fw_temperature_module_mounts: Dict[str, Set[BindMountInfo]]

    @classmethod
    def NO_MODULES_EXPECTED_RESULT(cls) -> "ModuleMounts":
        """Expected result when no module exists is no modules so no entrypoint scripts."""
        return cls({}, {}, {}, {}, {}, {})

    @classmethod
    def _generate_expected_mount_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, Set[BindMountInfo]]:
        return {
            container_name: {ENTRYPOINT_MOUNT} for container_name in container_names
        }

    @classmethod
    def _get_actual_mount_dict(
        cls, containers: List[Container]
    ) -> Dict[str, Set[BindMountInfo]]:
        return {container.name: set(get_mounts(container)) for container in containers}

    @classmethod
    def get_actual_results(
        cls: Type["ModuleMounts"], system_under_test: E2EHostSystem
    ) -> "ModuleMounts":
        """Load actual mounts from module containers."""
        return cls(
            hw_heater_shaker_module_mounts=cls._get_actual_mount_dict(
                system_under_test.module_containers.hardware_emulation_heater_shaker_modules
            ),
            fw_heater_shaker_module_mounts=cls._get_actual_mount_dict(
                system_under_test.module_containers.firmware_emulation_heater_shaker_modules
            ),
            hw_thermocycler_module_mounts=cls._get_actual_mount_dict(
                system_under_test.module_containers.hardware_emulation_thermocycler_modules
            ),
            fw_thermocycler_module_mounts=cls._get_actual_mount_dict(
                system_under_test.module_containers.firmware_emulation_thermocycler_modules
            ),
            fw_magnetic_module_mounts=cls._get_actual_mount_dict(
                system_under_test.module_containers.firmware_emulation_magnetic_modules
            ),
            fw_temperature_module_mounts=cls._get_actual_mount_dict(
                system_under_test.module_containers.firmware_emulation_temperature_modules
            ),
        )

    @classmethod
    def get_expected_results(
        cls: Type["ModuleMounts"], system_test_def: SystemTestDefinition
    ) -> "ModuleMounts":
        """Generate expected mount dicts for each module."""
        return cls(
            hw_heater_shaker_module_mounts=cls._generate_expected_mount_dict(
                system_test_def.module_configuration.hw_heater_shaker_module_names
            ),
            fw_heater_shaker_module_mounts=cls._generate_expected_mount_dict(
                system_test_def.module_configuration.fw_heater_shaker_module_names
            ),
            hw_thermocycler_module_mounts=cls._generate_expected_mount_dict(
                system_test_def.module_configuration.hw_thermocycler_module_names
            ),
            fw_thermocycler_module_mounts=cls._generate_expected_mount_dict(
                system_test_def.module_configuration.fw_thermocycler_module_names
            ),
            fw_magnetic_module_mounts=cls._generate_expected_mount_dict(
                system_test_def.module_configuration.fw_magnetic_module_names
            ),
            fw_temperature_module_mounts=cls._generate_expected_mount_dict(
                system_test_def.module_configuration.fw_temperature_module_names
            ),
        )


@dataclass
class ModuleBinaries(ModuleResultABC):
    """Ensures that all modules that are emulated at the hardware level have their binaries."""

    hw_thermocycler_module_binary_names: Dict[str, str]
    hw_heater_shaker_module_binary_names: Dict[str, str]

    @classmethod
    def NO_MODULES_EXPECTED_RESULT(cls) -> "ModuleBinaries":
        """If no hardware modules, no binaries."""
        return cls({}, {})

    @classmethod
    def _generate_heater_shaker_expected_binary_name_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, str]:
        return {
            container_name: ModulesExpectedBinaryNames.HEATER_SHAKER
            for container_name in container_names
        }

    @classmethod
    def _generate_thermocycler_expected_binary_name_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, str]:
        return {
            container_name: ModulesExpectedBinaryNames.THERMOCYCLER
            for container_name in container_names
        }

    @classmethod
    def _get_actual_binary_name_dict(
        cls, containers: List[Container]
    ) -> Dict[str, str]:
        return {
            container.name: exec_in_container(container, "ls /executable")
            for container in containers
        }

    @classmethod
    def get_actual_results(
        cls: Type["ModuleBinaries"], system_under_test: E2EHostSystem
    ) -> "ModuleBinaries":
        """Retrieve binary file names from module containers."""
        return cls(
            hw_thermocycler_module_binary_names=cls._get_actual_binary_name_dict(
                system_under_test.module_containers.hardware_emulation_thermocycler_modules
            ),
            hw_heater_shaker_module_binary_names=cls._get_actual_binary_name_dict(
                system_under_test.module_containers.hardware_emulation_heater_shaker_modules
            ),
        )

    @classmethod
    def get_expected_results(
        cls: Type["ModuleBinaries"], system_test_def: SystemTestDefinition
    ) -> "ModuleBinaries":
        """Generate expected names of binaries."""
        return cls(
            hw_thermocycler_module_binary_names=cls._generate_thermocycler_expected_binary_name_dict(
                system_test_def.module_configuration.hw_thermocycler_module_names
            ),
            hw_heater_shaker_module_binary_names=cls._generate_heater_shaker_expected_binary_name_dict(
                system_test_def.module_configuration.hw_heater_shaker_module_names
            ),
        )


@dataclass
class OpentronsModulesBuilderNamedVolumes(ModuleResultABC):
    """Ensures that the opentrons-modules-builder container has the correct volumes."""

    volumes: Set[NamedVolumeInfo]

    @classmethod
    def NO_MODULES_EXPECTED_RESULT(cls) -> "OpentronsModulesBuilderNamedVolumes":
        """No builder, no volumes."""
        return cls(set([]))

    @classmethod
    def get_actual_results(
        cls: Type["OpentronsModulesBuilderNamedVolumes"],
        system_under_test: E2EHostSystem,
    ) -> "OpentronsModulesBuilderNamedVolumes":
        """Load volumes from opentrons-module-builder container."""
        return cls(
            volumes=get_volumes(
                system_under_test.module_containers.opentrons_modules_builder
            )
        )

    @classmethod
    def get_expected_results(
        cls: Type["OpentronsModulesBuilderNamedVolumes"],
        system_test_def: SystemTestDefinition,
    ) -> "OpentronsModulesBuilderNamedVolumes":
        """Generate expected volumes for opentrons-modules-builder."""
        return cls(volumes=OPENTRONS_MODULES_BUILDER_NAMED_VOLUMES)


@dataclass
class ModuleResult(ModuleResultABC):
    """Collects all other Module results into a single data structure."""

    number_of_modules: int
    module_containers: ModuleContainerNames
    module_named_volumes: ModuleNamedVolumes
    module_mounts: ModuleMounts
    module_binaries: ModuleBinaries
    builder_named_volumes: OpentronsModulesBuilderNamedVolumes

    @classmethod
    def NO_MODULES_EXPECTED_RESULT(cls) -> "ModuleResult":
        """What no modules looks like."""
        return cls(
            number_of_modules=0,
            module_containers=ModuleContainerNames.NO_MODULES_EXPECTED_RESULT(),
            module_named_volumes=ModuleNamedVolumes.NO_MODULES_EXPECTED_RESULT(),
            module_mounts=ModuleMounts.NO_MODULES_EXPECTED_RESULT(),
            module_binaries=ModuleBinaries.NO_MODULES_EXPECTED_RESULT(),
            builder_named_volumes=OpentronsModulesBuilderNamedVolumes.NO_MODULES_EXPECTED_RESULT(),
        )

    @classmethod
    def get_expected_results(
        cls: Type["ModuleResult"], system_test_def: SystemTestDefinition
    ) -> "ModuleResult":
        """Get expected module results

        If no modules, expect to look like NO_MODULES_EXPECTED_RESULTS.
        Otherwise, call other get_expected_result methods.
        """
        if system_test_def.module_configuration.is_no_modules():
            return cls.NO_MODULES_EXPECTED_RESULT()
        else:
            return cls(
                number_of_modules=system_test_def.module_configuration.total_number_of_modules,
                module_containers=ModuleContainerNames.get_expected_results(
                    system_test_def
                ),
                module_named_volumes=ModuleNamedVolumes.get_expected_results(
                    system_test_def
                ),
                module_mounts=ModuleMounts.get_expected_results(system_test_def),
                module_binaries=ModuleBinaries.get_expected_results(system_test_def),
                builder_named_volumes=OpentronsModulesBuilderNamedVolumes.get_expected_results(
                    system_test_def
                ),
            )

    @classmethod
    def get_actual_results(
        cls: Type["ModuleResult"], system_under_test: E2EHostSystem
    ) -> "ModuleResult":
        """Get actual results."""
        return cls(
            number_of_modules=system_under_test.module_containers.number_of_modules,
            module_containers=ModuleContainerNames.get_actual_results(
                system_under_test
            ),
            module_named_volumes=ModuleNamedVolumes.get_actual_results(
                system_under_test
            ),
            module_mounts=ModuleMounts.get_actual_results(system_under_test),
            module_binaries=ModuleBinaries.get_actual_results(system_under_test),
            builder_named_volumes=OpentronsModulesBuilderNamedVolumes.get_actual_results(
                system_under_test
            ),
        )
