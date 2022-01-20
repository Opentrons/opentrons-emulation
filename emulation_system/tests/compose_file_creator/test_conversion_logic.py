"""Tests for converting input file to DockerComposeFile."""
import os
from typing import (
    Any,
    Dict,
    List,
    cast,
)
from unittest.mock import (
    MagicMock,
    patch,
)

import py
import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    FileDisambiguationError,
    convert_from_file,
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Network,
    Service,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DEFAULT_NETWORK_NAME,
    MountTypes,
)
from emulation_system.compose_file_creator.settings.images import (
    HeaterShakerModuleImages,
    MagneticModuleImages,
    RobotServerImages,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
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
    OT3_ID,
    SYSTEM_UNIQUE_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)

CONTAINER_NAME_TO_IMAGE = {
    OT2_ID: RobotServerImages().local_firmware_image_name,
    THERMOCYCLER_MODULE_ID: ThermocyclerModuleImages().local_hardware_image_name,
    HEATER_SHAKER_MODULE_ID: HeaterShakerModuleImages().remote_hardware_image_name,
    TEMPERATURE_MODULE_ID: TemperatureModuleImages().local_firmware_image_name,
    MAGNETIC_MODULE_ID: MagneticModuleImages().local_firmware_image_name,
}

SERVICE_NAMES = [
    OT2_ID,
    THERMOCYCLER_MODULE_ID,
    HEATER_SHAKER_MODULE_ID,
    TEMPERATURE_MODULE_ID,
    MAGNETIC_MODULE_ID,
]

EXTRA_MOUNT_PATH = "/var/log/log_files"
EMULATION_CONFIGURATION_DIR_1 = "em-config-dir-1"
EMULATION_CONFIGURATION_DIR_2 = "em-config-dir-2"
EMULATION_CONFIGURATION_FILE_NAME = "test-config.json"
TEMP_OPENTRONS_EMULATION_CONFIGURATION_FILE_NAME = "temp_test_configuration.json"


@pytest.fixture
def emulation_configuration_setup(
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
    tmpdir: py.path.local,
) -> OpentronsEmulationConfiguration:
    """Creates temporary directories for loading configuration files from.

    Stores these directories to OpentronsEmulationConfiguration.
    """
    root_dir = tmpdir.mkdir("emulation-configurations")
    path_1 = root_dir.mkdir(EMULATION_CONFIGURATION_DIR_1)
    path_2 = root_dir.mkdir(EMULATION_CONFIGURATION_DIR_2)
    test_conf = testing_opentrons_emulation_configuration

    test_conf.global_settings.emulation_configuration_file_locations.extend(
        [str(path_1), str(path_2)]
    )

    return test_conf


@pytest.fixture
def duplicate_emulation_files(
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
) -> OpentronsEmulationConfiguration:
    """Create file with same name in the 2 emulation_configuration_file_locations directories."""  # noqa: E501
    testing_opentrons_emulation_configuration.global_settings.emulation_configuration_file_locations = [  # noqa: E501
        "file_1",
        "file_2",
    ]
    return testing_opentrons_emulation_configuration


@pytest.fixture
def valid_configuration_load(
    tmpdir: py.path.local,
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
) -> OpentronsEmulationConfiguration:
    """Setup test to load a valid configuration."""
    root_dir = tmpdir.mkdir("emulation-configurations")
    path_1 = root_dir.mkdir(EMULATION_CONFIGURATION_DIR_1)
    test_conf = testing_opentrons_emulation_configuration
    test_conf.global_settings.emulation_configuration_file_locations.extend(
        [str(path_1)]
    )

    valid_dir = test_conf.global_settings.emulation_configuration_file_locations[0]
    file_path = os.path.join(valid_dir, EMULATION_CONFIGURATION_FILE_NAME)
    file = open(file_path, "w")
    # Technically an empty JSON is valid and we don't really care what is in the file
    # for this test.
    file.write("{}")
    file.close()
    return test_conf


@pytest.fixture
def version_only() -> Dict[str, Any]:
    """Input file with only a compose-file-version specified."""
    return {"compose-file-version": "4.0"}


@pytest.fixture
def extra_mounts_dir(tmpdir: py.path.local) -> str:
    """Creates temp path for extra mounts."""
    return str(tmpdir.mkdir("log_files"))


@pytest.fixture
def extra_mounts_and_opentrons(extra_mounts_dir: str, opentrons_dir: str) -> List[str]:
    """List with mount dir and opentrons-modules dir together.

    I have to build the list in a separate fixture because pytest-lazy-fixture does
    not evaluate when the function is in a list.
    So [lazy_fixture("opentrons"), lazy_fixture("extra_mounts_dir")]
    does not evaluate to ["path/to/opentrons", "path/to/extra_mounts_dir"]
    it instead evaluates to
    ["<LazyFixture "opentrons_dir">, <LazyFixture "extra_mounts_dir">] which
    causes the test to fail.
    See issue here: https://github.com/TvoroG/pytest-lazy-fixture/issues/24
    """
    return [extra_mounts_dir, opentrons_dir]


@pytest.fixture
def modules_dir_in_list(opentrons_modules_dir: str) -> List[str]:
    """Opentrons-modules repo in list.

    See extra_mounts_and_opentrons_modules docstring for more info.
    """
    return [opentrons_modules_dir]


@pytest.fixture
def opentrons_dir_in_list(opentrons_dir: str) -> List[str]:
    """Opentrons-modules repo in list.

    See extra_mounts_and_opentrons_modules docstring for more info.
    """
    return [opentrons_dir]


@pytest.fixture
def robot_with_mount(ot2_only: Dict[str, Any], extra_mounts_dir: str) -> Dict[str, Any]:
    """Robot dict with a mount added."""
    ot2_only["robot"]["extra-mounts"] = [
        {
            "name": "LOG_FILES",
            "type": MountTypes.DIRECTORY,
            "mount-path": EXTRA_MOUNT_PATH,
            "source-path": extra_mounts_dir,
        }
    ]
    return ot2_only


@pytest.fixture
def robot_with_mount_and_modules(
    robot_with_mount: Dict[str, Any],
    modules_only: Dict[str, Any],
) -> Dict[str, Any]:
    """Create config with robots and modules."""
    robot_with_mount.update(modules_only)

    return robot_with_mount


@pytest.fixture
def robot_with_mount_and_modules_services(
    robot_with_mount_and_modules: Dict[str, Any],
) -> Dict[str, Service]:
    """Get services from robot_and_modules."""
    return cast(
        Dict[str, Service], to_compose_file(robot_with_mount_and_modules).services
    )


@pytest.fixture
def with_system_unique_id_services(
    with_system_unique_id: Dict[str, Any]
) -> Dict[str, Service]:
    """Get services from with_system_unique_id."""
    return cast(Dict[str, Service], to_compose_file(with_system_unique_id).services)


def to_compose_file(input: Dict[str, Any]) -> RuntimeComposeFileModel:
    """Parses dict to SystemConfigurationModel then runs it through ConversionLayer."""
    return convert_from_obj(input)


def test_version(version_only: Dict[str, str]) -> None:
    """Confirms that version is set correctly on compose file."""
    assert to_compose_file(version_only).version == "4.0"


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


@pytest.mark.parametrize("service_name", SERVICE_NAMES)
def test_service_local_network(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Verify local network on individual services are correct."""
    assert robot_with_mount_and_modules_services[service_name].networks == [
        DEFAULT_NETWORK_NAME
    ]


def test_top_level_network(robot_and_modules: Dict[str, Any]) -> None:
    """Verify top level network is correct."""
    assert to_compose_file(robot_and_modules).networks == {
        DEFAULT_NETWORK_NAME: Network()
    }


def test_service_keys_with_system_unique_id(
    with_system_unique_id_services: Dict[str, Service]
) -> None:
    """Confirms service names are created correctly."""
    service_names = [
        OT2_ID,
        THERMOCYCLER_MODULE_ID,
        HEATER_SHAKER_MODULE_ID,
        TEMPERATURE_MODULE_ID,
        MAGNETIC_MODULE_ID,
        EMULATOR_PROXY_ID,
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
        SYSTEM_UNIQUE_ID
    ]


def test_top_level_network_with_system_unique_id(
    with_system_unique_id: Dict[str, Any]
) -> None:
    """Verify top level network is correct."""
    assert to_compose_file(with_system_unique_id).networks == {
        SYSTEM_UNIQUE_ID: Network()
    }


def test_emulation_proxy_not_created(ot2_only: Dict[str, Any]) -> None:
    """Verify emulator proxy is not created when there are no modules."""
    services = to_compose_file(ot2_only).services
    assert services is not None
    assert set(services.keys()) == {OT2_ID}


@pytest.mark.parametrize(
    "service_name",
    [
        THERMOCYCLER_MODULE_ID,
        TEMPERATURE_MODULE_ID,
        MAGNETIC_MODULE_ID,
        HEATER_SHAKER_MODULE_ID,
    ],
)
def test_module_depends_on(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Any]
) -> None:
    """Confirm that modules depend on emulator proxy."""
    assert robot_with_mount_and_modules_services[service_name].depends_on == [
        EMULATOR_PROXY_ID
    ]


def test_robot_depends_on(
    robot_with_mount_and_modules_services: Dict[str, Any]
) -> None:
    """Confirm that modules depend on emulator proxy."""
    assert robot_with_mount_and_modules_services[OT2_ID].depends_on is None


def test_robot_port(robot_with_mount_and_modules_services: Dict[str, Any]) -> None:
    """Confirm robot port string is created correctly."""
    assert robot_with_mount_and_modules_services[OT2_ID].ports == ["5000:31950"]


def test_robot_server_emulator_proxy_env_vars_added(
    robot_with_mount_and_modules_services: Dict[str, Any]
) -> None:
    """Confirm env vars are set correctly."""
    assert robot_with_mount_and_modules_services[OT2_ID].environment.__root__ == {
        "OT_SMOOTHIE_EMULATOR_URI": f"socket://{EMULATOR_PROXY_ID}:11000",
        "OT_EMULATOR_module_server": f'{{"host": "{EMULATOR_PROXY_ID}"}}',
    }
    assert (
        robot_with_mount_and_modules_services[MAGNETIC_MODULE_ID].environment.__root__
        == {}
    )
    assert (
        robot_with_mount_and_modules_services[
            HEATER_SHAKER_MODULE_ID
        ].environment.__root__
        == {}
    )
    assert (
        robot_with_mount_and_modules_services[
            TEMPERATURE_MODULE_ID
        ].environment.__root__
        == {}
    )
    assert (
        robot_with_mount_and_modules_services[
            THERMOCYCLER_MODULE_ID
        ].environment.__root__
        == {}
    )


def test_robot_server_emulator_proxy_env_vars_not_added(
    ot2_only: Dict[str, Any]
) -> None:
    """Confirm that env vars are not added to robot server when there are no modules."""
    robot_services = to_compose_file(ot2_only).services
    assert robot_services is not None
    robot_services_env = robot_services[OT2_ID].environment
    assert robot_services_env is not None
    assert robot_services_env.__root__ == {}


def test_ot3_feature_flag_added(ot3_only: Dict[str, Any]) -> None:
    """Confirm feature flag is added when robot is an OT3."""
    robot_services = to_compose_file(ot3_only).services
    assert robot_services is not None
    robot_services_env = robot_services[OT3_ID].environment
    assert robot_services_env is not None
    assert robot_services_env.__root__ == {
        "OT_API_FF_enableOT3HardwareController": "True"
    }


@pytest.mark.parametrize(
    "service_name",
    [
        THERMOCYCLER_MODULE_ID,
        TEMPERATURE_MODULE_ID,
        MAGNETIC_MODULE_ID,
        HEATER_SHAKER_MODULE_ID,
    ],
)
def test_module_command(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Any]
) -> None:
    """Confirm that modules depend on emulator proxy."""
    assert (
        robot_with_mount_and_modules_services[service_name].command == EMULATOR_PROXY_ID
    )


def test_robot_command(robot_with_mount_and_modules_services: Dict[str, Any]) -> None:
    """Confirm that modules depend on emulator proxy."""
    assert robot_with_mount_and_modules_services[OT2_ID].command is None


@patch("os.path.isabs")
@patch("os.path.isfile")
def test_emulation_configuration_file_not_found(
    mock_isabs: MagicMock,
    mock_isfile: MagicMock,
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
) -> None:
    """Test that correct error is thrown when configuration file cannot be found."""
    mock_isabs.return_value = False
    mock_isfile.return_value = False
    with pytest.raises(FileNotFoundError) as err:
        convert_from_file(
            testing_opentrons_emulation_configuration, EMULATION_CONFIGURATION_FILE_NAME
        )

    err.match(
        f"File {EMULATION_CONFIGURATION_FILE_NAME} not found in any specified "
        f"emulation_configuration_file_locations"
    )


@patch("os.path.isabs")
@patch("os.path.isfile")
def test_duplicate_emulation_configuration_file(
    mock_isfile: MagicMock,
    mock_isabs: MagicMock,
    duplicate_emulation_files: OpentronsEmulationConfiguration,
) -> None:
    """Test that correct error is thrown when configuration file cannot be found."""
    mock_isabs.return_value = False
    mock_isfile.return_value = True
    with pytest.raises(FileDisambiguationError) as err:
        convert_from_file(duplicate_emulation_files, EMULATION_CONFIGURATION_FILE_NAME)
    possible_locations = ", ".join(
        duplicate_emulation_files.global_settings.emulation_configuration_file_locations
    )
    err.match(f"Specified file found in multiple locations:" f" {possible_locations}")


def test_successful_conversion(
    valid_configuration_load: OpentronsEmulationConfiguration,
) -> None:
    """Test convert_from_file loads a valid configuration correctly."""
    convert_from_file(valid_configuration_load, EMULATION_CONFIGURATION_FILE_NAME)


# TODO: Add following tests:
#   - CAN network is created on OT3 breakout
#   - Port is exposed on robot server
#   - Module specifies correct proxy env var
#   - Module settings env var is correct
