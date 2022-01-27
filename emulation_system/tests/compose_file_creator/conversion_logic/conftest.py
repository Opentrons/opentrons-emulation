"""Conftest for conversion logic."""
from typing import (
    Any,
    Dict,
    List,
    cast,
)

import py
import pytest

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.compose_file_model import Service
from emulation_system.compose_file_creator.settings.config_file_settings import (
    MountTypes,
)
from emulation_system.compose_file_creator.settings.images import (
    HeaterShakerModuleImages,
    MagneticModuleImages,
    RobotServerImages,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
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
    settings = testing_opentrons_emulation_configuration.global_settings
    settings.emulation_configuration_file_locations = [
        "file_1",
        "file_2",
    ]
    return testing_opentrons_emulation_configuration


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
    """Get services from ot2_and_modules."""
    return cast(
        Dict[str, Service], convert_from_obj(robot_with_mount_and_modules).services
    )


@pytest.fixture
def with_system_unique_id_services(
    with_system_unique_id: Dict[str, Any]
) -> Dict[str, Service]:
    """Get services from with_system_unique_id."""
    return cast(Dict[str, Service], convert_from_obj(with_system_unique_id).services)
