"""Location for OT-3 e2e pytest functions."""
from typing import Callable

import pytest

from tests.e2e.fixtures.expected_bind_mounts import ExpectedBindMounts
from tests.e2e.fixtures.module_containers import ModuleContainers
from tests.e2e.fixtures.ot3_containers import OT3SystemUnderTest
from tests.e2e.test_mappings import get_e2e_test_parmeters
from tests.e2e.utilities.e2e_evaluator import E2EEvaluator
from tests.e2e.utilities.system_test_definition import SystemTestDefinition


@pytest.mark.parametrize("test_def", get_e2e_test_parmeters())
def test_e2e(
    test_def: SystemTestDefinition,
    ot3_model_under_test: Callable[[str], OT3SystemUnderTest],
    modules_under_test: Callable[[str], ModuleContainers],
    local_mounts_under_test: Callable[[str], ExpectedBindMounts],
) -> None:
    """Runs e2e tests for OT-3.

    If there is a failure, will log custom test output to console.
    """
    evaluator = E2EEvaluator(
        test_def, ot3_model_under_test(test_def.yaml_config_relative_path)
    )


    assert evaluator.generate_actual_result() == evaluator.generate_expected_result()

    # ot3_system = ot3_model_under_test(test_def.yaml_config_relative_path)
    # modules = modules_under_test(test_def.yaml_config_relative_path)
    # mounts = local_mounts_under_test(test_def.yaml_config_relative_path)
    # test_def.compare(ot3_system, modules, mounts)
    # assert not test_def.is_failure(), test_def.print_output()
    # print(test_def.print_output())
