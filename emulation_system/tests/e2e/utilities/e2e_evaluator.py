from tests.e2e.fixtures.ot3_containers import OT3SystemUnderTest
from tests.e2e.utilities.results.results import (
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


    @property
    def ot3_validation_required(self) -> bool:
        return self._test_def.ot3_firmware_builder_created

    def generate_expected_result(self) -> Result:

        if self.ot3_validation_required:
            expected_ot3_containers = OT3EmulatorContainers.init_all_exists()
        else:
            expected_ot3_containers = OT3EmulatorContainers.init_all_not_exists()

        expected_ot3_results = OT3Results(
            containers=expected_ot3_containers
        )

        return Result(ot3_results=expected_ot3_results)

    def generate_actual_result(self) -> Result:
        ...
        if self.ot3_validation_required:
            actual_ot3_containers = OT3EmulatorContainers.from_system_under_test(self._system_under_test)
        else:
            actual_ot3_containers = None

        actual_ot3_results = OT3Results(
            containers=actual_ot3_containers
        )
        return Result(ot3_results=actual_ot3_results)


if __name__ == "__main__":
    print(OT3EmulatorContainers.init_all_exists())
