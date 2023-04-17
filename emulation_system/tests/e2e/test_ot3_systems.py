"""Location for OT-3 e2e pytest functions."""
from typing import Callable

import pytest

from tests.e2e.fixtures.e2e_system import E2EHostSystem
from tests.e2e.fixtures.expected_bind_mounts import ExpectedBindMounts
from tests.e2e.fixtures.module_containers import ModuleContainers
from tests.e2e.fixtures.ot3_containers import OT3SystemUnderTest
from tests.e2e.test_mappings import get_e2e_test_parmeters
from tests.e2e.utilities.results.results import Result
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
    e2e_system = E2EHostSystem(
        ot3_containers=ot3_model_under_test(test_def.yaml_config_relative_path),
        module_containers=modules_under_test(test_def.yaml_config_relative_path),
        expected_binds_mounts=local_mounts_under_test(test_def.yaml_config_relative_path)
    )
    assert Result.get_actual_results(e2e_system) == Result.get_expected_results(test_def)
