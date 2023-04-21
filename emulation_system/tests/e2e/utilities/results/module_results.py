from dataclasses import dataclass
from typing import Dict, List, Set, Type

from docker.models.containers import Container  # type: ignore[import]

from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.utilities.consts import (
    ENTRYPOINT_MOUNT,
    BindMountInfo,
    ModulesExpectedBinaryNames,
    NamedVolumeInfo,
    OpentronsModulesBuilderNamedVolumesMap,
    OpentronsModulesEmulatorNamedVolumes,
)
from tests.e2e.utilities.helper_functions import (
    exec_in_container,
    get_container_names,
    get_mounts,
    get_volumes,
)
from tests.e2e.utilities.results.results_abc import Result


@dataclass
class ModuleContainerNames(Result):
    hw_heater_shaker_module_names: Set[str]
    fw_heater_shaker_module_names: Set[str]
    hw_thermocycler_module_names: Set[str]
    fw_thermocycler_module_names: Set[str]
    fw_magnetic_module_names: Set[str]
    fw_temperature_module_names: Set[str]

    emulator_proxy_name: str
    opentrons_modules_builder_name: str

    @classmethod
    def get_actual_results(
        cls: Type["ModuleContainerNames"], system_under_test: E2EHostSystem
    ) -> "ModuleContainerNames":
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
            emulator_proxy_name=system_under_test.module_containers.emulator_proxy.name,
            opentrons_modules_builder_name=system_under_test.module_containers.opentrons_modules_builder.name,
        )

    @classmethod
    def get_expected_results(
        cls: Type["ModuleContainerNames"], system_test_def: SystemTestDefinition
    ) -> "ModuleContainerNames":
        return cls(
            hw_heater_shaker_module_names=system_test_def.module_configuration.hw_heater_shaker_module_names,
            fw_heater_shaker_module_names=system_test_def.module_configuration.fw_heater_shaker_module_names,
            hw_thermocycler_module_names=system_test_def.module_configuration.hw_thermocycler_module_names,
            fw_thermocycler_module_names=system_test_def.module_configuration.fw_thermocycler_module_names,
            fw_magnetic_module_names=system_test_def.module_configuration.fw_magnetic_module_names,
            fw_temperature_module_names=system_test_def.module_configuration.fw_temperature_module_names,
            emulator_proxy_name=system_test_def.module_configuration.emulator_proxy_name,
            opentrons_modules_builder_name=system_test_def.module_configuration.opentrons_modules_builder_name,
        )


@dataclass
class ModuleNamedVolumes(Result):
    hw_heater_shaker_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    fw_heater_shaker_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    hw_thermocycler_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    fw_thermocycler_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    fw_magnetic_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]
    fw_temperature_module_named_volumes: Dict[str, Set[NamedVolumeInfo]]

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
class ModuleMounts(Result):
    hw_heater_shaker_module_mounts: Dict[str, Set[BindMountInfo]]
    fw_heater_shaker_module_mounts: Dict[str, Set[BindMountInfo]]
    hw_thermocycler_module_mounts: Dict[str, Set[BindMountInfo]]
    fw_thermocycler_module_mounts: Dict[str, Set[BindMountInfo]]
    fw_magnetic_module_mounts: Dict[str, Set[BindMountInfo]]
    fw_temperature_module_mounts: Dict[str, Set[BindMountInfo]]

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
class ModuleBinaries(Result):
    hw_thermocycler_module_binary_names: Dict[str, str]
    hw_heater_shaker_module_binary_names: Dict[str, str]

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
    def _generate_actual_binary_name_dict(
        cls, containers: List[Container]
    ) -> Dict[str, str]:
        print(containers)
        return {
            container.name: exec_in_container(container, "ls /executable")
            for container in containers
        }

    @classmethod
    def get_actual_results(
        cls: Type["ModuleBinaries"], system_under_test: E2EHostSystem
    ) -> "ModuleBinaries":
        return cls(
            hw_thermocycler_module_binary_names=cls._generate_actual_binary_name_dict(
                system_under_test.module_containers.hardware_emulation_thermocycler_modules
            ),
            hw_heater_shaker_module_binary_names=cls._generate_actual_binary_name_dict(
                system_under_test.module_containers.hardware_emulation_heater_shaker_modules
            ),
        )

    @classmethod
    def get_expected_results(
        cls: Type["ModuleBinaries"], system_test_def: SystemTestDefinition
    ) -> "ModuleBinaries":
        return cls(
            hw_thermocycler_module_binary_names=cls._generate_thermocycler_expected_binary_name_dict(
                system_test_def.module_configuration.hw_thermocycler_module_names
            ),
            hw_heater_shaker_module_binary_names=cls._generate_heater_shaker_expected_binary_name_dict(
                system_test_def.module_configuration.hw_heater_shaker_module_names
            ),
        )


@dataclass
class OpentronsModulesBuilderNamedVolumes(Result):

    volumes: Set[NamedVolumeInfo]

    @classmethod
    def get_actual_results(
        cls: Type["OpentronsModulesBuilderNamedVolumes"],
        system_under_test: E2EHostSystem,
    ) -> "OpentronsModulesBuilderNamedVolumes":
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
        return cls(
            volumes={
                OpentronsModulesBuilderNamedVolumesMap.HEATER_SHAKER,
                OpentronsModulesBuilderNamedVolumesMap.THERMOCYCLER,
            }
        )


@dataclass
class ModuleResult(Result):
    number_of_modules: int
    module_containers: ModuleContainerNames
    module_named_volumes: ModuleNamedVolumes
    module_mounts: ModuleMounts
    module_binaries: ModuleBinaries
    builder_named_volumes: OpentronsModulesBuilderNamedVolumes

    @classmethod
    def get_expected_results(
        cls: Type["ModuleResult"], system_test_def: SystemTestDefinition
    ) -> "ModuleResult":
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
