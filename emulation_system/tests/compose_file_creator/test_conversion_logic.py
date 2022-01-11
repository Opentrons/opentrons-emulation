"""Tests for converting input file to DockerComposeFile."""
from typing import (
    Any,
    Dict,
    cast,
)

import py
import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.conversion_functions import ToComposeFile
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Network,
    Service,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    MountTypes,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import (
    HeaterShakerModuleImages,
    MagneticModuleImages,
    OT2Images,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)
from emulation_system.consts import DOCKERFILE_DIR_LOCATION

ROBOT_NAME = "brobot"
THERMOCYCLER_NAME = "temperamental"
HEATER_SHAKER_NAME = "shakey-and-warm"
TEMPERATURE_MODULE_NAME = "t00-hot-to-handle"
MAGNETIC_MODULE_NAME = "fatal-attraction"

CONTAINER_NAME_TO_IMAGE = {
    ROBOT_NAME: OT2Images().remote_firmware_image_name,
    THERMOCYCLER_NAME: ThermocyclerModuleImages().local_firmware_image_name,
    HEATER_SHAKER_NAME: HeaterShakerModuleImages().remote_hardware_image_name,
    TEMPERATURE_MODULE_NAME: TemperatureModuleImages().remote_firmware_image_name,
    MAGNETIC_MODULE_NAME: MagneticModuleImages().remote_firmware_image_name,
}

SERVICE_NAMES = [
    ROBOT_NAME,
    THERMOCYCLER_NAME,
    HEATER_SHAKER_NAME,
    TEMPERATURE_MODULE_NAME,
    MAGNETIC_MODULE_NAME,
]

EXTRA_MOUNT_PATH = "/var/log/log_files"
SYSTEM_NETWORK_NAME = "testing-1-2-3"


@pytest.fixture
def version_only() -> Dict[str, Any]:
    """Input file with only a compose-file-version specified."""
    return {"compose-file-version": "4.0"}


@pytest.fixture
def system_network_name_only() -> Dict[str, Any]:
    """Return valid custom network name."""
    return {"system-network-name": "custom-network-name"}


@pytest.fixture
def invalid_system_network_name_only() -> Dict[str, Any]:
    """Return invalid custom network name."""
    return {"system-network-name": "__custom-network-name__"}


@pytest.fixture
def opentrons_dir(tmpdir: py.path.local) -> str:
    """Get path to temporary opentrons directory.

    Note that this variable is scoped to the test. So if you call the fixture from
    different places in the test the variable will be the same.
    """
    return str(tmpdir.mkdir("opentrons"))


@pytest.fixture
def extra_mounts_dir(tmpdir: py.path.local) -> str:
    """Creates temp path for extra mounts."""
    return str(tmpdir.mkdir("log_files"))


@pytest.fixture
def robot_and_modules(opentrons_dir: str, extra_mounts_dir: str) -> Dict[str, Any]:
    """Create config with robots and modules."""
    return {
        "system-network-name": SYSTEM_NETWORK_NAME,
        "robot": {
            "id": ROBOT_NAME,
            "hardware": Hardware.OT2,
            "source-type": SourceType.REMOTE,
            "source-location": "latest",
            "emulation-level": EmulationLevels.FIRMWARE,
            "extra-mounts": [
                {
                    "name": "LOG_FILES",
                    "type": MountTypes.DIRECTORY,
                    "mount-path": EXTRA_MOUNT_PATH,
                    "source-path": extra_mounts_dir,
                }
            ],
        },
        "modules": [
            {
                "id": THERMOCYCLER_NAME,
                "hardware": Hardware.THERMOCYCLER_MODULE,
                "source-type": SourceType.LOCAL,
                "source-location": opentrons_dir,
                "emulation-level": EmulationLevels.FIRMWARE,
            },
            {
                "id": HEATER_SHAKER_NAME,
                "hardware": Hardware.HEATER_SHAKER_MODULE,
                "source-type": SourceType.REMOTE,
                "source-location": "latest",
                "emulation-level": EmulationLevels.HARDWARE,
            },
            {
                "id": TEMPERATURE_MODULE_NAME,
                "hardware": Hardware.TEMPERATURE_MODULE,
                "source-type": SourceType.REMOTE,
                "source-location": "latest",
                "emulation-level": EmulationLevels.FIRMWARE,
            },
            {
                "id": MAGNETIC_MODULE_NAME,
                "hardware": Hardware.MAGNETIC_MODULE,
                "source-type": SourceType.REMOTE,
                "source-location": "latest",
                "emulation-level": EmulationLevels.FIRMWARE,
            },
        ],
    }


@pytest.fixture
def robot_and_modules_services(robot_and_modules: Dict[str, Any]) -> Dict[str, Service]:
    """Get services from robot_and_modules."""
    return cast(Dict[str, Service], to_compose_file(robot_and_modules).services)


def to_compose_file(input: Dict[str, Any]) -> RuntimeComposeFileModel:
    """Parses dict to SystemConfigurationModel then runs it through ConversionLayer."""
    return ToComposeFile.from_obj(input)


def test_version(version_only: Dict[str, str]) -> None:
    """Confirms that version is set correctly on compose file."""
    assert to_compose_file(version_only).version == "4.0"


def test_service_keys(robot_and_modules_services: Dict[str, Service]) -> None:
    """Confirms service names are created correctly."""
    assert set(robot_and_modules_services.keys()) == {
        ROBOT_NAME,
        THERMOCYCLER_NAME,
        HEATER_SHAKER_NAME,
        TEMPERATURE_MODULE_NAME,
        MAGNETIC_MODULE_NAME,
    }


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_tty(service_name: str, robot_and_modules_services: Dict[str, Service]) -> None:
    """Confirm tty is set to True."""
    assert robot_and_modules_services[service_name].tty


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_container_name(
    service_name: str, robot_and_modules_services: Dict[str, Service]
) -> None:
    """Verify container name matches service name."""
    assert robot_and_modules_services[service_name].container_name == service_name


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_image(
    service_name: str, robot_and_modules_services: Dict[str, Service]
) -> None:
    """Verify image name is correct."""
    assert (
        robot_and_modules_services[service_name].image
        == f"{CONTAINER_NAME_TO_IMAGE[service_name]}:latest"
    )


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_build(
    service_name: str, robot_and_modules_services: Dict[str, Service]
) -> None:
    """Verify build context and target are correct."""
    build = cast(BuildItem, robot_and_modules_services[service_name].build)
    assert build.context == DOCKERFILE_DIR_LOCATION
    assert build.target == CONTAINER_NAME_TO_IMAGE[service_name]


@pytest.mark.parametrize(
    "service_name", [HEATER_SHAKER_NAME, MAGNETIC_MODULE_NAME, TEMPERATURE_MODULE_NAME]
)
def test_service_without_bind_mounts(
    service_name: str, robot_and_modules_services: Dict[str, Service]
) -> None:
    """Verify services without volumes don't have volumes."""
    assert robot_and_modules_services[service_name].volumes is None


@pytest.mark.parametrize(
    "service_name,expected_source_path,expected_mount_path",
    [
        [ROBOT_NAME, lazy_fixture("extra_mounts_dir"), EXTRA_MOUNT_PATH],
        [THERMOCYCLER_NAME, lazy_fixture("opentrons_dir"), "/opentrons"],
    ],
)
def test_service_with_bind_mounts(
    service_name: str,
    expected_source_path: str,
    expected_mount_path: str,
    robot_and_modules_services: Dict[str, Service],
) -> None:
    """Verify services without volumes don't have volumes."""
    assert robot_and_modules_services[service_name].volumes == [
        f"{expected_source_path}:{expected_mount_path}"
    ]


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_local_network(
    service_name: str, robot_and_modules_services: Dict[str, Service]
) -> None:
    """Verify local network on individual services are correct."""
    assert robot_and_modules_services[service_name].networks == [SYSTEM_NETWORK_NAME]


def test_top_level_network(robot_and_modules: Dict[str, Any]) -> None:
    """Verify top level network is correct."""
    assert to_compose_file(robot_and_modules).networks == {
        SYSTEM_NETWORK_NAME: Network()
    }
