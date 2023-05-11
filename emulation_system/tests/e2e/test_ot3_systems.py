"""Location for OT-3 e2e pytest functions."""
from typing import Callable

import pytest

from tests.e2e.dataclass_helpers import convert_to_dict
from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.results.results import FinalResult
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.system_mappings import get_e2e_test_parameters




@pytest.mark.parametrize("test_def", get_e2e_test_parameters())
def test_e2e(
    test_def: SystemTestDefinition, e2e_host: Callable[[str], E2EHostSystem]
) -> None:
    """Runs e2e tests for OT-3.

    If there is a failure, will log custom test output to console.
    """
    e2e_system = e2e_host(test_def.yaml_config_relative_path)
    actual_results = convert_to_dict(
        FinalResult.get_actual_results(e2e_system)
    )
    expected_results = convert_to_dict(
        FinalResult.get_expected_results(test_def)
    )
    assert actual_results == expected_results
