from typing import Callable

import pytest

from tests.e2e.conftest import OT3System
from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.ot3_system_test_definition import OT3SystemTestDefinition

OT3_ONLY = OT3SystemTestDefinition(
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

OT3_AND_MODULES = OT3SystemTestDefinition(
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


@pytest.mark.parametrize(
    "test_def", [
        OT3_ONLY,
        OT3_AND_MODULES
    ],
    ids=[
        "ot3_only",
        "ot3_and_modules"
    ]
)
def test_e2e(
    test_def: OT3SystemTestDefinition,
    model_under_test: Callable
) -> None:
    ot3_system: OT3System = model_under_test(
        relative_path=test_def.yaml_config_relative_path
    )
    test_def.compare(ot3_system)
    print(test_def.print_output())
