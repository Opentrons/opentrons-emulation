"""Tests for converting input file to DockerComposeFile."""
from typing import (
    Any,
    Dict,
    List,
    cast,
)

import pytest

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator import (
    BuildItem,
    Service,
)
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.compose_file_model import Network
from emulation_system.consts import (
    DEFAULT_NETWORK_NAME,
    DOCKERFILE_DIR_LOCATION,
)
from tests.compose_file_creator.conftest import (
    EMULATOR_PROXY_ID,
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    SMOOTHIE_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)
from tests.compose_file_creator.conversion_logic.conftest import (
    CONTAINER_NAME_TO_IMAGE,
    SERVICE_NAMES,
)


# TODO: Add following tests:
#   - CAN network is created on OT3 breakout


def test_service_keys(
    robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Confirms service names are created correctly."""
    assert set(robot_with_mount_and_modules_services.keys()) == {
        OT2_ID,
        THERMOCYCLER_MODULE_ID,
        HEATER_SHAKER_MODULE_ID,
        TEMPERATURE_MODULE_ID,
        MAGNETIC_MODULE_ID,
        EMULATOR_PROXY_ID,
        SMOOTHIE_ID,
    }


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_tty(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Confirm tty is set to True."""
    assert robot_with_mount_and_modules_services[service_name].tty


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_container_name(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Verify container name matches service name."""
    assert (
            robot_with_mount_and_modules_services[service_name].container_name
            == service_name
    )


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_image(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Verify image name is correct."""
    assert (
            robot_with_mount_and_modules_services[service_name].image
            == f"{CONTAINER_NAME_TO_IMAGE[service_name]}:latest"
    )


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_build(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Verify build context and target are correct."""
    build = cast(BuildItem, robot_with_mount_and_modules_services[service_name].build)
    assert build.context == DOCKERFILE_DIR_LOCATION
    assert build.target == CONTAINER_NAME_TO_IMAGE[service_name]


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_local_network(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Verify local network on individual services are correct."""
    assert robot_with_mount_and_modules_services[service_name].networks == [
        DEFAULT_NETWORK_NAME
    ]


def test_top_level_network(
    ot2_and_modules: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Verify top level network is correct."""
    assert convert_from_obj(
        ot2_and_modules, testing_global_em_config, False
    ).networks == {DEFAULT_NETWORK_NAME: Network()}


def test_robot_port(robot_with_mount_and_modules_services: Dict[str, Any]) -> None:
    """Confirm robot port string is created correctly."""
    assert robot_with_mount_and_modules_services[OT2_ID].ports == ["5000:31950"]


def test_can_server_port_exposed(
    ot3_default: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm that when can-server-exposed-port is specified, ports are added to the can-server"""
    ot3_default["can-server-exposed-port"] = 9898
    runtime_compose_file_model = convert_from_obj(
        {"robot": ot3_default}, testing_global_em_config, False
    )
    can_server = runtime_compose_file_model.can_server
    assert can_server is not None
    assert can_server.ports is not None
    assert can_server.ports == ["9898:9898"]


def test_can_server_port_not_exposed(
    ot3_only: Dict[str, Any], testing_global_em_config: OpentronsEmulationConfiguration
) -> None:
    """Confirm that when can-server-exposed-port is not specified, ports are not added to the can-server"""
    runtime_compose_file_model = convert_from_obj(
        ot3_only, testing_global_em_config, False
    )
    can_server = runtime_compose_file_model.can_server
    assert can_server is not None
    assert can_server.ports is None


@pytest.mark.parametrize(
    "service_name, expected_value",
    [
        [THERMOCYCLER_MODULE_ID, ["--socket http://{EMULATOR_PROXY_ID}:10003"]],
        [TEMPERATURE_MODULE_ID, [EMULATOR_PROXY_ID]],
        [MAGNETIC_MODULE_ID, [EMULATOR_PROXY_ID]],
        [HEATER_SHAKER_MODULE_ID, ["--socket", f"http://{EMULATOR_PROXY_ID}:10004"]],
    ],
)
def test_module_command(
    service_name: str,
    expected_value: List[str],
    robot_with_mount_and_modules_services: Dict[str, Any],
) -> None:
    """Confirm that modules depend on emulator proxy."""
    assert robot_with_mount_and_modules_services[service_name].command == expected_value


def test_robot_command(robot_with_mount_and_modules_services: Dict[str, Any]) -> None:
    """Confirm that modules depend on emulator proxy."""
    assert robot_with_mount_and_modules_services[OT2_ID].command is None
