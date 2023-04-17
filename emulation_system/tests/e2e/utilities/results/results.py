from dataclasses import dataclass
from typing import (
    Optional,
    Type,
)

from tests.e2e.fixtures.e2e_system import E2EHostSystem
from tests.e2e.fixtures.expected_bind_mounts import ExpectedBindMounts
from tests.e2e.fixtures.module_containers import ModuleContainers

from tests.e2e.test_definition.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.consts import (

    MONOREPO_WHEELS,
)
from tests.e2e.utilities.helper_functions import (
    confirm_named_volume_exists,
)

from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.utilities.results.ot3_results import (
    OT3Results,
)
from tests.e2e.utilities.results.results_abc import (
    ResultsABC,
    TResults,
)

@dataclass
class ContainersWithMonorepoWheelVolume(ResultsABC):
    monorepo_builder_has_monorepo_wheel: bool
    emulator_proxy_has_monorepo_wheel: bool
    robot_server_has_monorepo_wheel: bool
    can_server_has_monorepo_wheel: bool
    state_manager_has_monorepo_wheel: bool

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            monorepo_builder_has_monorepo_wheel=True,
            emulator_proxy_has_monorepo_wheel=True,
            robot_server_has_monorepo_wheel=True,
            can_server_has_monorepo_wheel=True,
            state_manager_has_monorepo_wheel=True,
        )

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            monorepo_builder_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.monorepo_builder, MONOREPO_WHEELS),
            emulator_proxy_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.emulator_proxy, MONOREPO_WHEELS),
            robot_server_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.robot_server, MONOREPO_WHEELS),
            can_server_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.can_server, MONOREPO_WHEELS),
            state_manager_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.state_manager, MONOREPO_WHEELS),
        )


@dataclass
class BuilderContainers(ResultsABC):
    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool
    monorepo_builder_created: bool

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            ot3_firmware_builder_created=system_under_test.ot3_containers.ot3_firmware_builder_created,
            opentrons_modules_builder_created=system_under_test.ot3_containers.opentrons_modules_builder_created,
            monorepo_builder_created=system_under_test.ot3_containers.monorepo_builder_created,
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            ot3_firmware_builder_created=system_test_def.ot3_firmware_builder_created,
            opentrons_modules_builder_created=system_test_def.opentrons_modules_builder_created,
            monorepo_builder_created=system_test_def.monorepo_builder_created
        )


@dataclass
class LocalMounts(ResultsABC):
    monorepo_mounted: bool
    ot3_firmware_mounted: bool
    opentrons_modules_mounted: bool

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            monorepo_mounted=system_under_test.ot3_containers.local_monorepo_mounted,
            ot3_firmware_mounted=system_under_test.ot3_containers.local_ot3_firmware_mounted,
            opentrons_modules_mounted=system_under_test.ot3_containers.local_opentrons_modules_mounted,
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            monorepo_mounted=system_test_def.local_monorepo_mounted,
            ot3_firmware_mounted=system_test_def.local_ot3_firmware_mounted,
            opentrons_modules_mounted=system_test_def.local_opentrons_modules_mounted
        )
@dataclass
class SystemBuildArgs(ResultsABC):
    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            monorepo_build_args=system_under_test.ot3_containers.monorepo_build_args,
            ot3_firmware_build_args=system_under_test.ot3_containers.ot3_firmware_build_args,
            opentrons_modules_build_args=system_under_test.ot3_containers.opentrons_modules_build_args
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            monorepo_build_args=system_test_def.monorepo_build_args,
            ot3_firmware_build_args=system_test_def.ot3_firmware_build_args,
            opentrons_modules_build_args=system_test_def.opentrons_modules_build_args,
        )


@dataclass
class Result(ResultsABC):
    """Class containing all result values for e2e testing."""
    ot3_results: Optional[OT3Results]
    builder_containers: BuilderContainers
    local_mounts: LocalMounts
    system_build_args: SystemBuildArgs
    containers_with_monorepo_volumes: ContainersWithMonorepoWheelVolume

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            ot3_results=OT3Results.get_actual_results(system_under_test),
            builder_containers=BuilderContainers.get_actual_results(system_under_test),
            local_mounts=LocalMounts.get_actual_results(system_under_test),
            system_build_args=SystemBuildArgs.get_actual_results(system_under_test),
            containers_with_monorepo_volumes=ContainersWithMonorepoWheelVolume.get_actual_results(system_under_test)
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            ot3_results=(
                OT3Results.get_expected_results(system_test_def)
                if system_test_def.ot3_firmware_builder_created
                else None
            ),
            builder_containers=BuilderContainers.get_expected_results(system_test_def),
            local_mounts=LocalMounts.get_expected_results(system_test_def),
            system_build_args=SystemBuildArgs.get_expected_results(system_test_def),
            containers_with_monorepo_volumes=ContainersWithMonorepoWheelVolume.get_expected_results(system_test_def)
        )

class ResultBuilder:

    def __init__(self, ot3_system: E2EHostSystem, modules: ModuleContainers, local_mounts: ExpectedBindMounts) -> None:
        self._ot3_system =ot3_system
        self._modules =modules
        self._local_mounts =local_mounts
