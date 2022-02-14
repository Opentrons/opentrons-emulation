"""Tests related to bind mounts."""
from typing import (
    Dict,
    List,
)

import pytest

from emulation_system.compose_file_creator.output.compose_file_model import Service
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)


@pytest.mark.parametrize("service_name", [HEATER_SHAKER_MODULE_ID])
def test_service_without_bind_mounts(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Verify services without volumes don't have volumes."""
    assert robot_with_mount_and_modules_services[service_name].volumes is None


@pytest.mark.parametrize(
    "service_name,expected_mounts",
    [
        [
            OT2_ID,
            ["opentrons:/opentrons", "entrypoint.sh:/entrypoint.sh"],
        ],
        # Thermocycler should be bound to /opentrons-modules because it is using
        # hardware level emulation
        [
            THERMOCYCLER_MODULE_ID,
            ["opentrons-modules:/opentrons-modules", "entrypoint.sh:/entrypoint.sh"],
        ],
        [MAGNETIC_MODULE_ID, ["opentrons:/opentrons", "entrypoint.sh:/entrypoint.sh"]],
        [
            TEMPERATURE_MODULE_ID,
            ["opentrons:/opentrons", "entrypoint.sh:/entrypoint.sh"],
        ],
    ],
)
def test_service_with_bind_mounts(
    service_name: str,
    expected_mounts: List[str],
    robot_with_mount_and_modules_services: Dict[str, Service],
) -> None:
    """Verify services without volumes don't have volumes."""
    volumes = robot_with_mount_and_modules_services[service_name].volumes
    assert volumes is not None
    for mount in expected_mounts:
        assert any([mount in volume for volume in volumes])
