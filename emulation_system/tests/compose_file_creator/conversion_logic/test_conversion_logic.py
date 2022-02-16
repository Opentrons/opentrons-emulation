"""Tests for converting input file to DockerComposeFile."""
from typing import (
    Any,
    Dict,
    List,
    cast,
)

import pytest

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Network,
    Service,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DEFAULT_NETWORK_NAME,
)
from emulation_system.consts import (
    DOCKERFILE_DIR_LOCATION,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
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


@pytest.fixture
def version_only() -> Dict[str, Any]:
    """Input file with only a compose-file-version specified."""
    return {"compose-file-version": "4.0"}


# TODO: Add following tests:
#   - CAN network is created on OT3 breakout


def test_version(
    version_only: Dict[str, str],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirms that version is set correctly on compose file."""
    assert convert_from_obj(version_only, testing_global_em_config).version == "4.0"


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
    assert convert_from_obj(ot2_and_modules, testing_global_em_config).networks == {
        DEFAULT_NETWORK_NAME: Network()
    }


def test_robot_port(robot_with_mount_and_modules_services: Dict[str, Any]) -> None:
    """Confirm robot port string is created correctly."""
    assert robot_with_mount_and_modules_services[OT2_ID].ports == ["5000:31950"]


@pytest.mark.parametrize(
    "service_name, expected_value",
    [
        [THERMOCYCLER_MODULE_ID, ["--socket", f"http://{EMULATOR_PROXY_ID}:10003"]],
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
