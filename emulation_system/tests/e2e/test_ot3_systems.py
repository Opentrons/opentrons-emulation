import pytest

from tests.e2e.conftest import OT3Containers
from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.expected_bind_mounts import ExpectedBindMounts
from tests.e2e.utilities.module_containers import ModuleContainers
from tests.e2e.utilities.system_test_definition import SystemTestDefinition

OT3_ONLY = SystemTestDefinition(
    yaml_config_relative_path="samples/common_use_cases/basic/ot3_only.yaml",
    monorepo_builder_created=True,
    ot3_firmware_builder_created=True,
    opentrons_modules_builder_created=False,
    local_monorepo_mounted=False,
    local_ot3_firmware_mounted=False,
    local_opentrons_modules_mounted=False,
    monorepo_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    ot3_firmware_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    opentrons_modules_build_args=BuildArgConfigurations.NO_BUILD_ARGS,
)

OT3_AND_MODULES = SystemTestDefinition(
    yaml_config_relative_path="samples/common_use_cases/basic/ot3_and_modules.yaml",
    monorepo_builder_created=True,
    ot3_firmware_builder_created=True,
    opentrons_modules_builder_created=True,
    local_monorepo_mounted=False,
    local_ot3_firmware_mounted=False,
    local_opentrons_modules_mounted=False,
    monorepo_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    ot3_firmware_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    opentrons_modules_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
)

OT3_FIRMWARE_DEV = SystemTestDefinition(
    yaml_config_relative_path="samples/common_use_cases/bind/ot3_firmware.yaml",
    monorepo_builder_created=True,
    ot3_firmware_builder_created=True,
    opentrons_modules_builder_created=False,
    local_monorepo_mounted=True,
    local_ot3_firmware_mounted=True,
    local_opentrons_modules_mounted=False,
    # Build args are latest because the source code will end up be overwritten by
    # the bind mount
    monorepo_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    ot3_firmware_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    opentrons_modules_build_args=BuildArgConfigurations.NO_BUILD_ARGS,
)


@pytest.mark.parametrize(
    "test_def",
    [OT3_ONLY, OT3_AND_MODULES, OT3_FIRMWARE_DEV],
    ids=["ot3_only", "ot3_and_modules", "ot3_firmware_dev"],
)
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
