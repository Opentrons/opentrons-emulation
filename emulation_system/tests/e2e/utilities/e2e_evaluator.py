from tests.e2e.fixtures.ot3_containers import OT3SystemUnderTest
from tests.e2e.utilities.results.results import (
    BuilderContainers,
    OT3EmulatorContainers,
    OT3Results,
    Result,
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
    @property
    def ot3_validation_required(self) -> bool:
        return self._test_def.ot3_firmware_builder_created

    def generate_expected_result(self) -> Result:
        expected_ot3_containers = self._evaluate_expected_ot3_containers()
        expected_ot3_results = OT3Results(containers=expected_ot3_containers)
        builder_containers = self._evaluate_expected_builder_containers()

        return Result(
            ot3_results=expected_ot3_results,
            builder_containers=builder_containers
        )

    def generate_actual_result(self) -> Result:
        ...
        if self.ot3_validation_required:
            actual_ot3_containers = OT3EmulatorContainers.from_system_under_test(self._system_under_test)
        else:
            actual_ot3_containers = None

        actual_ot3_results = OT3Results(
            containers=actual_ot3_containers
        )
        return Result(
            ot3_results=actual_ot3_results,
            builder_containers=BuilderContainers.from_system_under_test(self._system_under_test)
        )


if __name__ == "__main__":
    print(OT3EmulatorContainers.init_all_exists())
