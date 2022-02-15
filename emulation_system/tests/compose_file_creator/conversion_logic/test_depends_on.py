"""Tests related to depends_on property of services."""

from typing import Any, Dict

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from tests.compose_file_creator.conftest import (
    EMULATOR_PROXY_ID,
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    OT3_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)


@pytest.mark.parametrize(
    "service_name",
    [
        THERMOCYCLER_MODULE_ID,
        TEMPERATURE_MODULE_ID,
        MAGNETIC_MODULE_ID,
        HEATER_SHAKER_MODULE_ID,
        OT2_ID,
    ],
)
def test_emulator_proxy_in_depends_on(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Any]
) -> None:
    """Confirm that modules depend on emulator proxy."""
    assert (
        EMULATOR_PROXY_ID
        in robot_with_mount_and_modules_services[service_name].depends_on
    )


@pytest.mark.parametrize(
    "config, service_id",
    [
        [lazy_fixture("ot2_only"), OT2_ID],
        [lazy_fixture("ot3_only"), OT3_ID],
    ],
)
def test_robots_only_emulator_proxy_in_depends_on(
    config: Dict[str, Any],
    service_id: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm that OT2 and OT3 depends on emulator proxy when there are no modules.

    Have to check for membership in list because depends_on will have the smoothie
    dependency for OT2
    """
    services = convert_from_obj(config, testing_global_em_config).services
    assert services is not None
    depends_on = services[service_id].depends_on
    assert isinstance(depends_on, list)
    assert EMULATOR_PROXY_ID in depends_on
