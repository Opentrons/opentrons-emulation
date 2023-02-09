import pytest

from tests.e2e.test_mappings import get_e2e_test_parmeters
from tests.e2e.utilities.expected_bind_mounts import ExpectedBindMounts
from tests.e2e.utilities.module_containers import ModuleContainers
from tests.e2e.utilities.ot3_containers import OT3Containers
from tests.e2e.utilities.system_test_definition import SystemTestDefinition


@pytest.mark.parametrize("test_def", get_e2e_test_parmeters())
def test_e2e(
    test_def: SystemTestDefinition,
    ot3_model_under_test,
    modules_under_test,
    local_mounts_under_test,
) -> None:
    ot3_system: OT3Containers = ot3_model_under_test(
        relative_path=test_def.yaml_config_relative_path
    )
    modules: ModuleContainers = modules_under_test(test_def.yaml_config_relative_path)
    mounts: ExpectedBindMounts = local_mounts_under_test(
        test_def.yaml_config_relative_path
    )
    test_def.compare(ot3_system, modules, mounts)
    assert not test_def.is_failure(), test_def.print_output()
    print(test_def.print_output())
