from dataclasses import dataclass
from typing import Container, Dict, List, Set, Type

from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.utilities.consts import (
    ENTRYPOINT_MOUNT,
    ExpectedMount,
    ExpectedNamedVolume,
    ModulesExpectedBinaryNames,
    OpentronsModulesEmulatorNamedVolumes,
)
from tests.e2e.utilities.helper_functions import (
    cast_mount_dict_to_expected_mount,
    cast_volume_dict_to_expected_volume,
    confirm_named_volume_exists,
    exec_in_container,
    get_mounts,
    get_volumes,
)
from tests.e2e.utilities.results.results_abc import ResultsABC, TResults


@dataclass
class ModuleContainerNames(ResultsABC):
    hw_heater_shaker_module_names: Set[str]
    fw_heater_shaker_module_names: Set[str]
    hw_thermocycler_module_names: Set[str]
    fw_thermocycler_module_names: Set[str]
    fw_magnetic_module_names: Set[str]
    fw_temperature_module_names: Set[str]

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            hw_heater_shaker_module_names=system_under_test.module_containers.hardware_emulation_heater_shaker_module_names,
            fw_heater_shaker_module_names=system_under_test.module_containers.firmware_emulation_heater_shaker_module_names,
            hw_thermocycler_module_names=system_under_test.module_containers.hardware_emulation_thermocycler_module_names,
            fw_thermocycler_module_names=system_under_test.module_containers.firmware_emulation_thermocycler_module_names,
            fw_magnetic_module_names=system_under_test.module_containers.firmware_emulation_magnetic_module_names,
            fw_temperature_module_names=system_under_test.module_containers.firmware_emulation_temperature_module_names,
        )

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            hw_heater_shaker_module_names=system_test_def.module_configuration.hw_heater_shaker_module_names,
            fw_heater_shaker_module_names=system_test_def.module_configuration.fw_heater_shaker_module_names,
            hw_thermocycler_module_names=system_test_def.module_configuration.hw_thermocycler_module_names,
            fw_thermocycler_module_names=system_test_def.module_configuration.fw_thermocycler_module_names,
            fw_magnetic_module_names=system_test_def.module_configuration.fw_magnetic_module_names,
            fw_temperature_module_names=system_test_def.module_configuration.fw_temperature_module_names,
        )


@dataclass
class ModuleNamedVolumes(ResultsABC):
    hw_heater_shaker_module_named_volumes: Dict[str, Set[ExpectedNamedVolume]]
    fw_heater_shaker_module_named_volumes: Dict[str, Set[ExpectedNamedVolume]]
    hw_thermocycler_module_named_volumes: Dict[str, Set[ExpectedNamedVolume]]
    fw_thermocycler_module_named_volumes: Dict[str, Set[ExpectedNamedVolume]]
    fw_magnetic_module_named_volumes: Dict[str, Set[ExpectedNamedVolume]]
    fw_temperature_module_named_volumes: Dict[str, Set[ExpectedNamedVolume]]

    @classmethod
    def _generate_heater_shaker_hw_expected_named_volume_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, Set[ExpectedNamedVolume]]:
        return {
            container_name: {
                ExpectedNamedVolume(
                    VOLUME_NAME="heater_shaker_executable", DEST_PATH="/executable"
                )
            }
            for container_name in container_names
        }

    @classmethod
    def _generate_thermocycler_hw_expected_named_volume_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, Set[ExpectedNamedVolume]]:
        return {
            container_name: {
                ExpectedNamedVolume(
                    VOLUME_NAME="thermocycler_executable", DEST_PATH="/executable"
                )
            }
            for container_name in container_names
        }

    @classmethod
    def _generate_fw_expected_named_volume_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, Set[ExpectedNamedVolume]]:
        return {
            container_name: {
                ExpectedNamedVolume(VOLUME_NAME="monorepo-wheels", DEST_PATH="/dist")
            }
            for container_name in container_names
        }

    @classmethod
    def _get_actual_named_volumes_dict(
        cls, containers: List[Container]
    ) -> Dict[str, Set[ExpectedNamedVolume]]:
        return {
            container.name: set(
                [
                    cast_volume_dict_to_expected_volume(volume)
                    for volume in get_volumes(container)
                ]
            )
            for container in containers
        }

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
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
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
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
class ModuleMounts(ResultsABC):
    hw_heater_shaker_module_mounts: Dict[str, ExpectedMount]
    fw_heater_shaker_module_mounts: Dict[str, ExpectedMount]
    hw_thermocycler_module_mounts: Dict[str, ExpectedMount]
    fw_thermocycler_module_mounts: Dict[str, ExpectedMount]
    fw_magnetic_module_mounts: Dict[str, ExpectedMount]
    fw_temperature_module_mounts: Dict[str, ExpectedMount]

    @classmethod
    def _generate_expected_mount_dict(
        cls, container_names: Set[str]
    ) -> Dict[str, Set[ExpectedMount]]:
        return {
            container_name: {ENTRYPOINT_MOUNT} for container_name in container_names
        }

    @classmethod
    def _get_actual_mount_dict(
        cls, containers: List[Container]
    ) -> Dict[str, Set[ExpectedNamedVolume]]:
        return {
            container.name: set(
                [
                    cast_mount_dict_to_expected_mount(mount)
                    for mount in get_mounts(container)
                ]
            )
            for container in containers
        }

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
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
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
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
class ModuleBinaries(ResultsABC):
    hw_thermocycler_module_binary_names: Dict[str, str]
    hw_heater_shaker_module_binary_names: Dict[str, str]

    @classmethod
    def _generate_heater_shaker_expected_binary_name_dict(cls, container_names: Set[str]) -> Dict[str, str]:
        return {
            container_name: ModulesExpectedBinaryNames.HEATER_SHAKER
            for container_name in container_names
        }

    @classmethod
    def _generate_thermocycler_expected_binary_name_dict(cls, container_names: Set[str]) -> Dict[str, str]:
        return {
            container_name: ModulesExpectedBinaryNames.THERMOCYCLER
            for container_name in container_names
        }

    @classmethod
    def _generate_actual_binary_name_dict(cls, containers: List[Container]) -> Dict[str, str]:
        print(containers)
        return {
            container.name: exec_in_container(container, "ls /executable")
            for container in containers
        }

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            hw_thermocycler_module_binary_names=cls._generate_actual_binary_name_dict(system_under_test.module_containers.hardware_emulation_thermocycler_modules),
            hw_heater_shaker_module_binary_names=cls._generate_actual_binary_name_dict(system_under_test.module_containers.hardware_emulation_heater_shaker_modules)
        )

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            hw_thermocycler_module_binary_names=cls._generate_thermocycler_expected_binary_name_dict(
                system_test_def.module_configuration.hw_thermocycler_module_names
                ),
            hw_heater_shaker_module_binary_names=cls._generate_heater_shaker_expected_binary_name_dict(
                system_test_def.module_configuration.hw_heater_shaker_module_names
                ),
        )


@dataclass
class OpentronsModulesBuilderNamedVolumes(ResultsABC):

    heater_shaker_volume_exists: bool
    thermocycler_volume_exists: bool

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            heater_shaker_volume_exists=confirm_named_volume_exists(
                system_under_test.module_containers.modules_builder,
                OpentronsModulesEmulatorNamedVolumes.HEATER_SHAKER
            ),
            thermocycler_volume_exists=confirm_named_volume_exists(
                system_under_test.module_containers.modules_builder,
                OpentronsModulesEmulatorNamedVolumes.THERMOCYCLER
            )
        )

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            heater_shaker_volume_exists=True,
            thermocycler_volume_exists=True
        )


@dataclass
class ModuleResults(ResultsABC):
    number_of_modules: int
    module_containers: ModuleContainerNames
    module_named_volumes: ModuleNamedVolumes
    module_mounts: ModuleMounts
    module_binaries: ModuleBinaries
    # builder_named_volumes: OpentronsModulesBuilderNamedVolumes

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            number_of_modules=system_test_def.module_configuration.total_number_of_modules,
            module_containers=ModuleContainerNames.get_expected_results(
                system_test_def
            ),
            module_named_volumes=ModuleNamedVolumes.get_expected_results(
                system_test_def
            ),
            module_mounts=ModuleMounts.get_expected_results(system_test_def),
            module_binaries=ModuleBinaries.get_expected_results(system_test_def)
        )

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            number_of_modules=system_under_test.module_containers.number_of_modules,
            module_containers=ModuleContainerNames.get_actual_results(
                system_under_test
            ),
            module_named_volumes=ModuleNamedVolumes.get_actual_results(
                system_under_test
            ),
            module_mounts=ModuleMounts.get_actual_results(system_under_test),
            module_binaries=ModuleBinaries.get_actual_results(system_under_test)
        )
