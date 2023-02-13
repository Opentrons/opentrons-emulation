import argparse
import json
from typing import (
    Dict,
    List,
)

import pytest
from _pytest.mark.structures import ParameterSet

from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.system_test_definition import SystemTestDefinition

_TEST_DEFS: Dict[str, SystemTestDefinition] = {
    "ot3_remote":       SystemTestDefinition(
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
    ),
    "ot3_firmware_dev": SystemTestDefinition(
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
    ),
    "ot3_and_modules":  SystemTestDefinition(
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
    ),
}


def get_e2e_test_parmeters() -> List[ParameterSet]:
    return [
        pytest.param(mapping, id=mapping.test_id) for mapping in _TEST_DEFS.values()
    ]


def get_test_ids() -> str:
    return json.dumps([mapping.test_id for mapping in _TEST_DEFS.values()])


def get_test_path(test_id: str) -> str:
    return _TEST_DEFS[test_id].yaml_config_relative_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interaction layer for opentrons-emulation e2e test mappings."
    )
    subparsers = parser.add_subparsers(dest="command")

    test_ids = subparsers.add_parser(
        "get-test-ids", help="Get list of available test IDs"
    )

    test_path = subparsers.add_parser(
        "get-test-path", help="Get path for test based on test ID"
    )
    test_path.add_argument("test-id", type=str, help="Pass a test id")
    args = parser.parse_args()

    if args.command == "get-test-ids":
        print(get_test_ids())
    elif args.command == "get-test-path":
        print(get_test_path(vars(args)["test-id"]))
