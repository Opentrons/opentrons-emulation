from tests.e2e.fixtures.ot3_containers import OT3SystemUnderTest
from tests.e2e.utilities.consts import OT3FirmwareEmulatorNamedVolumesMap
from tests.e2e.utilities.results.results import (
    BuilderContainers,
    LocalMounts,
    OT3EmulatorContainers,
    OT3EmulatorNamedVolumes,
    OT3Results,
    Result,
    SystemBuildArgs,
)
from tests.e2e.utilities.system_test_definition import SystemTestDefinition

class E2EEvaluator:
    def __init__(
        self,
        test_def: SystemTestDefinition,
        system_under_test: OT3SystemUnderTest
    ):
        self._test_def = test_def
        self._system_under_test = system_under_test

    def _evaluate_expected_ot3_containers(self) -> OT3EmulatorContainers:
        return (
            OT3EmulatorContainers.init_all_exists()
            if self.ot3_validation_required
            else OT3EmulatorContainers.init_all_not_exists()
        )

    def _evaluate_expected_builder_containers(self) -> BuilderContainers:
        return BuilderContainers(
            ot3_firmware_builder_created=self._test_def.ot3_firmware_builder_created,
            opentrons_modules_builder_created=self._test_def.opentrons_modules_builder_created,
            monorepo_builder_created=self._test_def.monorepo_builder_created
        )

    def _evaluate_expected_local_mounts(self) -> LocalMounts:
        return LocalMounts(
            monorepo_mounted=self._test_def.local_monorepo_mounted,
            ot3_firmware_mounted=self._test_def.local_ot3_firmware_mounted,
            opentrons_modules_mounted=self._test_def.local_opentrons_modules_mounted
        )

    def _evaluate_expected_system_build_args(self) -> SystemBuildArgs:
        return SystemBuildArgs(
            monorepo_build_args=self._test_def.monorepo_build_args,
            ot3_firmware_build_args=self._test_def.ot3_firmware_build_args,
            opentrons_modules_build_args=self._test_def.opentrons_modules_build_args,
        )

    @staticmethod
    def _evaluate_expected_ot3_emulator_named_volumes() -> OT3EmulatorNamedVolumes:
        return OT3EmulatorNamedVolumes(
            head_volume_exists=True,
            gantry_x_volume_exists=True,
            gantry_y_volume_exists=True,
            gripper_volume_exists=True,
            pipettes_volume_exists=True,
            bootloader_volume_exists=True
        )
    @property
    def ot3_validation_required(self) -> bool:
        return self._test_def.ot3_firmware_builder_created

    def generate_expected_result(self) -> Result:
        expected_ot3_containers = self._evaluate_expected_ot3_containers()
        expected_ot3_emulator_volumes = self._evaluate_expected_ot3_emulator_named_volumes()
        expected_ot3_results = OT3Results(
            containers=expected_ot3_containers,
            emulator_volumes=expected_ot3_emulator_volumes
        )
        builder_containers = self._evaluate_expected_builder_containers()
        local_mounts = self._evaluate_expected_local_mounts()
        expected_build_args = self._evaluate_expected_system_build_args()

        return Result(
            ot3_results=expected_ot3_results,
            builder_containers=builder_containers,
            local_mounts=local_mounts,
            system_build_args=expected_build_args
        )

    def generate_actual_result(self) -> Result:
        ...
        if self.ot3_validation_required:
            actual_ot3_containers = OT3EmulatorContainers.from_system_under_test(self._system_under_test)
            actual_ot3_emulator_volumes = OT3EmulatorNamedVolumes.from_system_under_test(self._system_under_test)
        else:
            actual_ot3_containers = None
            actual_ot3_emulator_volumes = None

        actual_ot3_results = OT3Results(
            containers=actual_ot3_containers,
            emulator_volumes=actual_ot3_emulator_volumes
        )
        return Result(
            ot3_results=actual_ot3_results,
            builder_containers=BuilderContainers.from_system_under_test(self._system_under_test),
            local_mounts=LocalMounts.from_system_under_test(self._system_under_test),
            system_build_args=SystemBuildArgs.from_system_under_test(self._system_under_test)
        )


if __name__ == "__main__":
    print(OT3EmulatorContainers.init_all_exists())
