from dataclasses import dataclass
from typing import (
    Optional,
    Set,
    Type,
)

from tests.e2e.fixtures.e2e_system import E2EHostSystem
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.utilities.consts import (
    ExpectedMount,
    ExpectedNamedVolume,
)
from tests.e2e.utilities.results.results_abc import (
    ResultsABC,
    TResults,
)


@dataclass
class OpentronsModulesBuilderNamedVolumes(ResultsABC):

    heater_shaker_volume_exists: bool
    thermocycler_volume_exists: bool

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        ...

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        ...


@dataclass
class ModuleInfo:
    container_name: str
    named_volumes: Set[ExpectedNamedVolume]
    mounts: Set[ExpectedMount]
    expected_binary: Optional[str]


@dataclass
class ModuleConfiguration:
    total_number_of_modules: int
    hw_heater_shakers: Set[ModuleInfo]
    hw_thermocyclers: Set[ModuleInfo]
    fw_heater_shakers: Set[ModuleInfo]
    fw_thermocyclers: Set[ModuleInfo]
    fw_magnetic_modules: Set[ModuleInfo]
    fw_temperature_modules: Set[ModuleInfo]


@dataclass
class ModuleResults(ResultsABC):
    module_configuration: ModuleConfiguration
    # builder_named_volumes: OpentronsModulesNamedVolumes

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        module_conf = system_test_def.module_configuration
        return cls(
            module_configuration=module_conf
        )

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        ...
