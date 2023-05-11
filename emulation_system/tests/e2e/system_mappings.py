"""Module for storing e2e test configurations."""

import argparse
import json
from typing import Dict, List

import pytest
from _pytest.mark.structures import ParameterSet

from tests.e2e.test_definition.build_arg_configurations import BuildArgConfigurations
from tests.e2e.test_definition.system_test_definition import (
    ModuleConfiguration,
    SystemTestDefinition,
)

OT3_REMOTE = SystemTestDefinition(
    test_id="ot3_remote",
    yaml_config_relative_path="samples/ci/ot3/ot3_remote.yaml",
    monorepo_builder_created=True,
    ot3_firmware_builder_created=True,
    opentrons_modules_builder_created=False,
    local_monorepo_mounted=False,
    local_ot3_firmware_mounted=False,
    local_opentrons_modules_mounted=False,
    monorepo_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    ot3_firmware_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    opentrons_modules_build_args=BuildArgConfigurations.NO_BUILD_ARGS,
    module_configuration=ModuleConfiguration.NO_MODULES(),
)

OT3_FIRMWARE_DEV = SystemTestDefinition(
    test_id="ot3_firmware_dev",
    yaml_config_relative_path="samples/ci/team_specific_setups/ot3_firmware_development.yaml",
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
    module_configuration=ModuleConfiguration.NO_MODULES(),
)

OT3_AND_MODULES = SystemTestDefinition(
    test_id="ot3_and_modules",
    yaml_config_relative_path="samples/ci/ot3/ot3_and_modules.yaml",
    monorepo_builder_created=True,
    ot3_firmware_builder_created=True,
    opentrons_modules_builder_created=True,
    local_monorepo_mounted=False,
    local_ot3_firmware_mounted=False,
    local_opentrons_modules_mounted=False,
    monorepo_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    ot3_firmware_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    opentrons_modules_build_args=BuildArgConfigurations.LATEST_BUILD_ARGS,
    module_configuration=ModuleConfiguration(
        total_number_of_modules=6,
        hw_heater_shaker_module_names={"ot3-and-modules-heater-shaker"},
        hw_thermocycler_module_names={"ot3-and-modules-thermocycler"},
        fw_heater_shaker_module_names={"ot3-and-modules-heater-shaker-fw"},
        fw_thermocycler_module_names={"ot3-and-modules-thermocycler-fw"},
        fw_magnetic_module_names={"ot3-and-modules-magdeck"},
        fw_temperature_module_names={"ot3-and-modules-tempdeck"},
    ),
)

_TEST_DEFS: Dict[str, SystemTestDefinition] = {
    "ot3_remote": OT3_REMOTE,
    "ot3_firmware_dev": OT3_FIRMWARE_DEV,
    "ot3_and_modules": OT3_AND_MODULES,
}


def get_e2e_test_parameters() -> List[ParameterSet]:
    """Generates pytest parameters based off of above list of TestMapping objects."""
    return [
        pytest.param(mapping, id=mapping.test_id) for mapping in _TEST_DEFS.values()
    ]


def get_test_ids() -> str:
    """Generates list of test ids to past to pytest.mark.parameterize with above get_e2e_test_parameters."""
    return json.dumps([mapping.test_id for mapping in _TEST_DEFS.values()])


def get_test_path(test_id: str) -> str:
    """Gets relative path to test for passed test id."""
    return _TEST_DEFS[test_id].yaml_config_relative_path
