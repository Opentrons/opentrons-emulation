"""Top-level results that will end up being compared."""

from dataclasses import dataclass
from typing import Optional, Type

from tests.e2e.consts import MONOREPO_WHEEL_VOLUME
from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.helper_functions import confirm_named_volume_exists
from tests.e2e.results.module_results import ModuleResult
from tests.e2e.results.ot3_results import OT3Result
from tests.e2e.results.results_abc import ResultABC
from tests.e2e.test_definition.build_arg_configurations import BuildArgConfigurations
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition


@dataclass
class ContainersWithMonorepoWheelVolume(ResultABC):
    """Validate that containers that are supposed to have the monorepo wheel volume do."""

    monorepo_builder_has_monorepo_wheel: bool
    emulator_proxy_has_monorepo_wheel: bool
    robot_server_has_monorepo_wheel: bool
    can_server_has_monorepo_wheel: bool
    state_manager_has_monorepo_wheel: bool

    @classmethod
    def get_expected_results(
        cls: Type["ContainersWithMonorepoWheelVolume"],
        system_test_def: SystemTestDefinition,
    ) -> "ContainersWithMonorepoWheelVolume":
        """Set everything to True since they should all have the volume."""
        return cls(
            monorepo_builder_has_monorepo_wheel=True,
            emulator_proxy_has_monorepo_wheel=True,
            robot_server_has_monorepo_wheel=True,
            can_server_has_monorepo_wheel=True,
            state_manager_has_monorepo_wheel=True,
        )

    @classmethod
    def get_actual_results(
        cls: Type["ContainersWithMonorepoWheelVolume"], system_under_test: E2EHostSystem
    ) -> "ContainersWithMonorepoWheelVolume":
        """For each container, check that it has expected volume."""
        return cls(
            monorepo_builder_has_monorepo_wheel=confirm_named_volume_exists(
                system_under_test.default_containers.monorepo_builder,
                MONOREPO_WHEEL_VOLUME,
            ),
            emulator_proxy_has_monorepo_wheel=confirm_named_volume_exists(
                system_under_test.module_containers.emulator_proxy,
                MONOREPO_WHEEL_VOLUME,
            ),
            robot_server_has_monorepo_wheel=confirm_named_volume_exists(
                system_under_test.default_containers.robot_server, MONOREPO_WHEEL_VOLUME
            ),
            can_server_has_monorepo_wheel=confirm_named_volume_exists(
                system_under_test.ot3_containers.can_server, MONOREPO_WHEEL_VOLUME
            ),
            state_manager_has_monorepo_wheel=confirm_named_volume_exists(
                system_under_test.ot3_containers.state_manager, MONOREPO_WHEEL_VOLUME
            ),
        )


@dataclass
class BuilderContainers(ResultABC):
    """Confirm builder containers are created when they are supposed to be."""

    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool
    monorepo_builder_created: bool

    @classmethod
    def get_actual_results(
        cls: Type["BuilderContainers"], system_under_test: E2EHostSystem
    ) -> "BuilderContainers":
        """Check if each builder container exists."""
        return cls(
            ot3_firmware_builder_created=system_under_test.ot3_containers.ot3_firmware_builder_created,
            opentrons_modules_builder_created=system_under_test.module_containers.opentrons_modules_builder_created,
            monorepo_builder_created=system_under_test.default_containers.monorepo_builder_created,
        )

    @classmethod
    def get_expected_results(
        cls: Type["BuilderContainers"], system_test_def: SystemTestDefinition
    ) -> "BuilderContainers":
        """Load expected container existence directly from system_test_def."""
        return cls(
            ot3_firmware_builder_created=system_test_def.ot3_firmware_builder_created,
            opentrons_modules_builder_created=system_test_def.opentrons_modules_builder_created,
            monorepo_builder_created=system_test_def.monorepo_builder_created,
        )


@dataclass
class LocalMounts(ResultABC):
    """Confirm source code is mounted in when it is supposed to be."""

    monorepo_mounted: bool
    ot3_firmware_mounted: bool
    opentrons_modules_mounted: bool

    @classmethod
    def get_actual_results(
        cls: Type["LocalMounts"], system_under_test: E2EHostSystem
    ) -> "LocalMounts":
        """Check if local code is mounted."""
        return cls(
            monorepo_mounted=system_under_test.default_containers.local_monorepo_mounted,
            ot3_firmware_mounted=system_under_test.ot3_containers.local_ot3_firmware_mounted,
            opentrons_modules_mounted=system_under_test.module_containers.local_opentrons_modules_mounted,
        )

    @classmethod
    def get_expected_results(
        cls: Type["LocalMounts"], system_test_def: SystemTestDefinition
    ) -> "LocalMounts":
        """Check if local code is supposed to be mounted.

        Pull directly from system test def.
        """
        return cls(
            monorepo_mounted=system_test_def.local_monorepo_mounted,
            ot3_firmware_mounted=system_test_def.local_ot3_firmware_mounted,
            opentrons_modules_mounted=system_test_def.local_opentrons_modules_mounted,
        )


@dataclass
class SystemBuildArgs(ResultABC):
    """Validate build args are correct."""

    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations

    @classmethod
    def get_actual_results(
        cls: Type["SystemBuildArgs"], system_under_test: E2EHostSystem
    ) -> "SystemBuildArgs":
        """Load build args from e2e system."""
        return cls(
            monorepo_build_args=system_under_test.default_containers.monorepo_build_args,
            ot3_firmware_build_args=system_under_test.ot3_containers.ot3_firmware_build_args,
            opentrons_modules_build_args=system_under_test.module_containers.opentrons_modules_build_args,
        )

    @classmethod
    def get_expected_results(
        cls: Type["SystemBuildArgs"], system_test_def: SystemTestDefinition
    ) -> "SystemBuildArgs":
        """Load expected build args from system test def"""
        return cls(
            monorepo_build_args=system_test_def.monorepo_build_args,
            ot3_firmware_build_args=system_test_def.ot3_firmware_build_args,
            opentrons_modules_build_args=system_test_def.opentrons_modules_build_args,
        )


@dataclass
class FinalResult(ResultABC):
    """Class containing all result values for e2e testing."""

    ot3_results: Optional[OT3Result]
    module_results: Optional[ModuleResult]
    builder_containers: BuilderContainers
    local_mounts: LocalMounts
    system_build_args: SystemBuildArgs
    containers_with_monorepo_volumes: ContainersWithMonorepoWheelVolume
    robot_server_exists: bool
    monorepo_builder_exists: bool

    @classmethod
    def get_actual_results(
        cls: Type["FinalResult"], system_under_test: E2EHostSystem
    ) -> "FinalResult":
        """Get actual final result for comparison."""
        return cls(
            ot3_results=OT3Result.get_actual_results(system_under_test),
            builder_containers=BuilderContainers.get_actual_results(system_under_test),
            local_mounts=LocalMounts.get_actual_results(system_under_test),
            system_build_args=SystemBuildArgs.get_actual_results(system_under_test),
            containers_with_monorepo_volumes=ContainersWithMonorepoWheelVolume.get_actual_results(
                system_under_test
            ),
            module_results=ModuleResult.get_actual_results(system_under_test),
            robot_server_exists=system_under_test.default_containers.robot_server
            is not None,
            monorepo_builder_exists=system_under_test.default_containers.monorepo_builder
            is not None,
        )

    @classmethod
    def get_expected_results(
        cls: Type["FinalResult"], system_test_def: SystemTestDefinition
    ) -> "FinalResult":
        """Get expected final result for comparison."""
        return cls(
            ot3_results=(
                OT3Result.get_expected_results(system_test_def)
                if system_test_def.ot3_firmware_builder_created
                else None
            ),
            builder_containers=BuilderContainers.get_expected_results(system_test_def),
            local_mounts=LocalMounts.get_expected_results(system_test_def),
            system_build_args=SystemBuildArgs.get_expected_results(system_test_def),
            containers_with_monorepo_volumes=ContainersWithMonorepoWheelVolume.get_expected_results(
                system_test_def
            ),
            module_results=ModuleResult.get_expected_results(system_test_def),
            robot_server_exists=True,
            monorepo_builder_exists=True,
        )
