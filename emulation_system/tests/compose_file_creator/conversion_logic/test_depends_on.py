"""Tests related to depends_on property of services."""

from typing import (
    Any,
    Dict,
)

import pytest

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
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


def test_ot2_emulator_proxy_not_in_depends_on(ot2_only: Dict[str, Any]) -> None:
    """Confirm that OT2 does not depend on emulator proxy when there are no modules.

    Have to check for membership in list because depends_on will have the smoothie
    dependency for OT2
    """
    services = convert_from_obj(ot2_only).services
    assert services is not None
    depends_on = services[OT2_ID].depends_on
    assert isinstance(depends_on, list)
    assert EMULATOR_PROXY_ID not in depends_on


def test_ot3_emulator_proxy_not_in_depends_on(ot3_only: Dict[str, Any]) -> None:
    """Confirm that OT3 does not depend on emulator proxy when there are no modules.

    OT3 should not have an other dependencies so make sure depends_on is None
    """
    services = convert_from_obj(ot3_only).services
    assert services is not None
    assert services[OT3_ID].depends_on is None
