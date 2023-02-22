"""Tests related to system-unique-id property."""

from typing import Any, Dict, cast

import pytest

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.images import (
    MonorepoBuilderImage,
    OpentronsModulesBuilderImage,
)
from emulation_system.compose_file_creator.output.compose_file_model import Network
from emulation_system.consts import DEFAULT_NETWORK_NAME
from tests.conftest import (
    EMULATOR_PROXY_ID,
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    SMOOTHIE_ID,
    SYSTEM_UNIQUE_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)
from tests.validation_helper_functions import SERVICE_NAMES


@pytest.fixture
def with_system_unique_id_services(
    with_system_unique_id: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Dict[str, Service]:
    """Get services from with_system_unique_id."""
    return cast(
        Dict[str, Service],
        convert_from_obj(
            with_system_unique_id, testing_global_em_config, False
        ).services,
    )


def test_service_keys_with_system_unique_id(
    with_system_unique_id_services: Dict[str, Service]
) -> None:
    """Confirms service names are created correctly."""
    service_names = [
        OT2_ID,
        f"{THERMOCYCLER_MODULE_ID}-1",
        f"{HEATER_SHAKER_MODULE_ID}-1",
        f"{TEMPERATURE_MODULE_ID}-1",
        f"{MAGNETIC_MODULE_ID}-1",
        MonorepoBuilderImage.image_name,
        OpentronsModulesBuilderImage.image_name,
        EMULATOR_PROXY_ID,
        SMOOTHIE_ID,
    ]

    service_names_with_system_unique_id = {
        f"{SYSTEM_UNIQUE_ID}-{service_name}" for service_name in service_names
    }
    assert (
        set(with_system_unique_id_services.keys())
        == service_names_with_system_unique_id
    )


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_container_name_with_system_unique_id(
    service_name: str, with_system_unique_id_services: Dict[str, Service]
) -> None:
    """Verify container name matches service name."""
    modded_service_name = f"{SYSTEM_UNIQUE_ID}-{service_name}"
    assert (
        with_system_unique_id_services[modded_service_name].container_name
        == modded_service_name
    )


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_local_network_with_system_unique_id(
    service_name: str, with_system_unique_id_services: Dict[str, Service]
) -> None:
    """Verify local network on individual services are correct."""
    modded_service_name = f"{SYSTEM_UNIQUE_ID}-{service_name}"
    assert with_system_unique_id_services[modded_service_name].networks == [
        f"{SYSTEM_UNIQUE_ID}-{DEFAULT_NETWORK_NAME}"
    ]


def test_top_level_network_with_system_unique_id(
    with_system_unique_id: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Verify top level network is correct."""
    assert convert_from_obj(
        with_system_unique_id, testing_global_em_config, False
    ).networks == {f"{SYSTEM_UNIQUE_ID}-{DEFAULT_NETWORK_NAME}": Network()}
