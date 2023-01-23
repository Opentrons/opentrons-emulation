from typing import Callable

from tests.e2e.conftest import (
    BuildArgConfigurations,
    OT3System,
    OT3SystemValidationModel,
)

OT3_ONLY_RELATIVE_PATH = "samples/common_use_cases/basic/ot3_only.yaml"

EXPECTED_VALUE = OT3SystemValidationModel(
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


def test_ot3_only(model_under_test: Callable) -> None:
    ot3_system: OT3System = model_under_test(relative_path=OT3_ONLY_RELATIVE_PATH)
    EXPECTED_VALUE.compare(ot3_system)
