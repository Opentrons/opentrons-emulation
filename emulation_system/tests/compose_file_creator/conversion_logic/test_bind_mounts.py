"""Tests related to bind mounts."""
from typing import Dict, List

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.output.compose_file_model import Service
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)
from tests.compose_file_creator.conversion_logic.conftest import EXTRA_MOUNT_PATH


@pytest.mark.parametrize("service_name", [HEATER_SHAKER_MODULE_ID])
def test_service_without_bind_mounts(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Verify services without volumes don't have volumes."""
    assert robot_with_mount_and_modules_services[service_name].volumes is None


@pytest.mark.parametrize(
    "service_name,expected_source_path,expected_mount_path",
    [
        [
            OT2_ID,
            lazy_fixture("extra_mounts_and_opentrons"),
            [EXTRA_MOUNT_PATH, "/opentrons"],
        ],
        # Thermocycler should be bound to /opentrons-modules because it is using
        # hardware level emulation
        [
            THERMOCYCLER_MODULE_ID,
            lazy_fixture("modules_dir_in_list"),
            ["/opentrons-modules"],
        ],
        [MAGNETIC_MODULE_ID, lazy_fixture("opentrons_dir_in_list"), ["/opentrons"]],
        [TEMPERATURE_MODULE_ID, lazy_fixture("opentrons_dir_in_list"), ["/opentrons"]],
    ],
)
def test_service_with_bind_mounts(
    service_name: str,
    expected_source_path: List[str],
    expected_mount_path: List[str],
    robot_with_mount_and_modules_services: Dict[str, Service],
) -> None:
    """Verify services without volumes don't have volumes."""
    assert robot_with_mount_and_modules_services[service_name].volumes == [
        f"{expected_source_path[i]}:{expected_mount_path[i]}"
        for i, _ in enumerate(expected_source_path)
    ]
