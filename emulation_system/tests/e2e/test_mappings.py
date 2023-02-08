import json
from typing import List

import pytest
from _pytest.mark.structures import ParameterSet

from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.system_test_definition import SystemTestDefinition

_TEST_DEFS = [
    SystemTestDefinition(
        test_id="ot3_only",
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
    ),
    SystemTestDefinition(
        test_id="ot3_firmware_dev",
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
    ),
    SystemTestDefinition(
        test_id="ot3_and_modules",
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
    ),
]


def get_e2e_test_parmeters() -> List[ParameterSet]:
    return [pytest.param(mapping, id=mapping.test_id) for mapping in _TEST_DEFS]


def get_test_ids() -> str:
    return json.dumps([mapping.test_id for mapping in _TEST_DEFS])


if __name__ == "__main__":
    print(get_test_ids())
