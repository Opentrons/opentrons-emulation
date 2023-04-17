"""Module for storing e2e test configurations."""

import argparse
import json
from typing import Dict, List

import pytest
from _pytest.mark.structures import ParameterSet

from tests.e2e.test_definition.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.results.module_results import (
    ModuleConfiguration,
    ModuleInfo,
)
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.utilities.consts import (
    ENTRYPOINT_MOUNT,
    ExpectedNamedVolume,
    MONOREPO_WHEELS,
    OpentronsModulesEmulatorNamedVolumes,
)

NO_MODULES = ModuleConfiguration(
    total_number_of_modules=0,
    hw_heater_shakers=set(),
    hw_thermocyclers=set(),
    fw_heater_shakers=set(),
    fw_thermocyclers=set(),
    fw_magnetic_modules=set(),
    fw_temperature_modules=set(),
)

_TEST_DEFS: Dict[str, SystemTestDefinition] = {
    "ot3_remote": SystemTestDefinition(
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
        module_configuration=NO_MODULES
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
        module_configuration=NO_MODULES
    ),
    "ot3_and_modules": SystemTestDefinition(
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
            hw_heater_shakers={
                ModuleInfo(
                    container_name="ot3-and-modules-heater-shaker",
                    named_volumes={
                        OpentronsModulesEmulatorNamedVolumes.HEATER_SHAKER
                    },
                    mounts={
                        ENTRYPOINT_MOUNT
                    }
                )
            },
            hw_thermocyclers={
                ModuleInfo(
                    container_name="ot3-and-modules-thermocycler",
                    named_volumes={
                        OpentronsModulesEmulatorNamedVolumes.THERMOCYCLER
                    },
                    mounts={
                        ENTRYPOINT_MOUNT
                    }
                )
            },
            fw_heater_shakers={
                        ModuleInfo(
                    container_name="ot3-and-modules-heater-shaker-fw",
                    named_volumes={
                        MONOREPO_WHEELS
                    },
                    mounts={
                        ENTRYPOINT_MOUNT
                    }
                ),
            },
                fw_thermocyclers={
            ModuleInfo(
                    container_name="ot3-and-modules-thermocycler-fw",
                    named_volumes={
                        MONOREPO_WHEELS
                    },
                    mounts={
                        ENTRYPOINT_MOUNT
                    }
                ),
            },
            fw_magnetic_modules={
            ModuleInfo(
                    container_name="ot3-and-modules-magdeck",
                    named_volumes={
                        MONOREPO_WHEELS
                    },
                    mounts={
                        ENTRYPOINT_MOUNT
                    }
                ),
            },
            fw_temperature_modules={
            ModuleInfo(
                    container_name="ot3-and-modules-tempdeck",
                    named_volumes={
                        MONOREPO_WHEELS
                    },
                    mounts={
                        ENTRYPOINT_MOUNT
                    }
                )
            }
        )
    ),
}


def get_e2e_test_parmeters() -> List[ParameterSet]:
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
