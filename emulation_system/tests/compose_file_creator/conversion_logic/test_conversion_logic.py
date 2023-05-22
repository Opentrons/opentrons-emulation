"""Tests for converting input file to DockerComposeFile."""
from typing import Any, Dict, Optional, cast

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.config_file_settings import OT3Hardware
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.compose_file_model import Network
from emulation_system.consts import DEFAULT_NETWORK_NAME, DOCKERFILE_DIR_LOCATION
from tests.conftest import (
    EMULATOR_PROXY_ID,
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    MONOREPO_BUILDER_ID,
    OPENTRONS_MODULES_BUILDER_ID,
    OT2_ID,
    OT3_FIRMWARE_BUILDER_ID,
    OT3_ID,
    OT3_STATE_MANAGER_ID,
    SMOOTHIE_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)
from tests.validation_helper_functions import CONTAINER_NAME_TO_IMAGE, SERVICE_NAMES


# TODO: Add following tests:
#   - CAN network is created on OT3 breakout


@pytest.mark.parametrize(
    "config, is_ot3",
    [[lazy_fixture("ot2_and_modules"), False], [lazy_fixture("ot3_and_modules"), True]],
)
def test_service_keys(
    config: Dict[str, Any],
    is_ot3: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirms service names are created correctly."""
    config_file = convert_from_obj(config, testing_global_em_config, dev=False)

    default_values = {
        f"{THERMOCYCLER_MODULE_ID}-1",
        f"{HEATER_SHAKER_MODULE_ID}-1",
        f"{TEMPERATURE_MODULE_ID}-1",
        f"{MAGNETIC_MODULE_ID}-1",
        MONOREPO_BUILDER_ID,
        OPENTRONS_MODULES_BUILDER_ID,
        EMULATOR_PROXY_ID,
    }

    if is_ot3:
        default_values.update([item.value for item in OT3Hardware.__members__.values()])
        default_values.add("can-server")
        default_values.add(OT3_ID)
        default_values.add(OT3_FIRMWARE_BUILDER_ID)
        default_values.add(OT3_STATE_MANAGER_ID)
    else:
        default_values.add(OT2_ID)
        default_values.add(SMOOTHIE_ID)

    assert config_file.services is not None
    assert set(config_file.services.keys()) == default_values


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_tty(
    service_name: str,
    ot2_and_modules: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm tty is set to True."""
    services = convert_from_obj(
        ot2_and_modules, testing_global_em_config, dev=False
    ).services
    assert services is not None
    assert services[service_name].tty


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_container_name(
    service_name: str,
    ot2_and_modules: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Verify container name matches service name."""
    services = convert_from_obj(
        ot2_and_modules, testing_global_em_config, dev=False
    ).services
    assert services is not None
    assert services[service_name].container_name == service_name


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_image(
    service_name: str,
    ot2_and_modules: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Verify image name is correct."""
    services = convert_from_obj(
        ot2_and_modules, testing_global_em_config, dev=False
    ).services
    assert services is not None
    assert services[service_name].image == CONTAINER_NAME_TO_IMAGE[service_name]


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_build(
    service_name: str,
    ot2_and_modules: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Verify build context and target are correct."""
    services = convert_from_obj(
        ot2_and_modules, testing_global_em_config, dev=False
    ).services
    assert services is not None
    build = cast(BuildItem, services[service_name].build)
    assert build.context == DOCKERFILE_DIR_LOCATION
    assert build.target == CONTAINER_NAME_TO_IMAGE[service_name]


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_local_network(
    service_name: str,
    ot2_and_modules: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Verify local network on individual services are correct."""
    services = convert_from_obj(
        ot2_and_modules, testing_global_em_config, dev=False
    ).services
    assert services is not None
    assert services[service_name].networks == [DEFAULT_NETWORK_NAME]


def test_top_level_network(
    ot2_and_modules: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Verify top level network is correct."""
    networks = convert_from_obj(
        ot2_and_modules, testing_global_em_config, dev=False
    ).networks
    assert networks is not None
    assert networks == {DEFAULT_NETWORK_NAME: Network()}


def test_robot_port(
    ot2_and_modules: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm robot port string is created correctly."""
    services = convert_from_obj(
        ot2_and_modules, testing_global_em_config, dev=False
    ).services
    assert services is not None
    assert services[OT2_ID].ports == ["5000:31950"]


@pytest.mark.parametrize("can_port", [None, 10000])
def test_can_server_port_exposed(
    can_port: Optional[str],
    ot3_only: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm that when can-server-exposed-port is specified, ports are added to the can-server"""
    if can_port is not None:
        ot3_only["robot"]["can-server-exposed-port"] = can_port

    runtime_compose_file_model = convert_from_obj(
        ot3_only, testing_global_em_config, False
    )
    can_server = runtime_compose_file_model.can_server
    assert can_server is not None
    assert can_server.ports is not None

    if can_port is not None:

        assert can_server.ports == [f"{can_port}:9898"]
    else:
        assert can_server.ports == ["9898:9898"]
