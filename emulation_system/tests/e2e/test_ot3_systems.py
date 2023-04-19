"""Location for OT-3 e2e pytest functions."""
from typing import Callable

import pytest

from tests.e2e.docker_interface.e2e_system import (
    DefaultContainers,
    E2EHostSystem,
    ExpectedBindMounts,
)
from tests.e2e.docker_interface.module_containers import ModuleContainers
from tests.e2e.docker_interface.ot3_containers import OT3SystemUnderTest
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.test_mappings import get_e2e_test_parameters
from tests.e2e.utilities.results.results import FinalResult


@pytest.mark.parametrize("test_def", get_e2e_test_parameters())
def test_e2e(
    test_def: SystemTestDefinition,
    ot3_model_under_test: Callable[[str], OT3SystemUnderTest],
    modules_under_test: Callable[[str], ModuleContainers],
    local_mounts_under_test: Callable[[str], ExpectedBindMounts],
    default_containers_under_test: Callable[[str], DefaultContainers],
) -> None:
    """Runs e2e tests for OT-3.

    If there is a failure, will log custom test output to console.
    """
    e2e_system = E2EHostSystem(
        ot3_containers=ot3_model_under_test(test_def.yaml_config_relative_path),
        module_containers=modules_under_test(test_def.yaml_config_relative_path),
        expected_binds_mounts=local_mounts_under_test(
            test_def.yaml_config_relative_path
        ),
        default_containers=default_containers_under_test(
            test_def.yaml_config_relative_path
        ),
    )
    assert (
            FinalResult.get_actual_results(e2e_system).__dict__
            == FinalResult.get_expected_results(test_def).__dict__
    )
