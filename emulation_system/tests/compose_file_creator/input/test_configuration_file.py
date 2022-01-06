"""Tests for SystemConfigurationModel class.

Note: Do not need to test matching module names because module names cannot be the same
by definition of dict.
"""
import os
import pathlib
from typing import Dict

import pytest
from pydantic import ValidationError

from emulation_system.compose_file_creator.input.configuration_file import (
    DuplicateHardwareNameError,
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    OT2InputModel,
)
from tests.conftest import get_test_resources_dir

INVALID_CONFIG_DIR_PATH = os.path.join(
    get_test_resources_dir(), "invalid_configurations"
)
VALID_CONFIG_DIR_PATH = os.path.join(get_test_resources_dir(), "valid_configurations")
MATCHING_ROBOT_AND_MODULE_NAMES_PATH = os.path.join(
    INVALID_CONFIG_DIR_PATH, "matching_robot_and_module_names.json"
)
MATCHING_MODULE_NAMES_PATH = os.path.join(
    INVALID_CONFIG_DIR_PATH, "matching_module_names.json"
)
INVALID_NAME_FORMAT_PATH = os.path.join(
    INVALID_CONFIG_DIR_PATH, "invalid_name_format.json"
)
MODULES_ONLY_PATH = os.path.join(VALID_CONFIG_DIR_PATH, "modules_only.json")
ROBOT_ONLY_PATH = os.path.join(VALID_CONFIG_DIR_PATH, "robot_only.json")
ROBOT_AND_MODULES_PATH = os.path.join(VALID_CONFIG_DIR_PATH, "robot_and_modules.json")
EMPTY_ROBOT_KEY_PATH = os.path.join(VALID_CONFIG_DIR_PATH, "empty_robot_key.json")
EMPTY_MODULES_KEY_PATH = os.path.join(VALID_CONFIG_DIR_PATH, "empty_modules_key.json")


@pytest.fixture
def extra_mounts(tmp_path: pathlib.Path, robot_only: Dict) -> Dict:
    """Configuration of a robot with extra bind mounts."""
    datadog_dir = tmp_path / "Datadog"
    datadog_dir.mkdir()
    datadog_file = datadog_dir / "log.txt"
    datadog_file.write_text("test")

    log_dir = tmp_path / "Log"
    log_dir.mkdir()

    robot_only["robot"]["my-robot"]["extra-mounts"] = [
        {
            "name": "DATADOG",
            "source-path": str(datadog_file),
            "mount-path": "/datadog/log.txt",
            "type": "file",
        },
        {
            "name": "LOG_FILES",
            "source-path": str(log_dir),
            "mount-path": "/var/log/opentrons/",
            "type": "directory",
        },
    ]
    return robot_only


@pytest.fixture
def invalid_mount_name(extra_mounts: Dict) -> Dict:
    """Configuration with an invalid mount name."""
    extra_mounts["robot"]["my-robot"]["extra-mounts"][0]["name"] = "data-dog"
    return extra_mounts


def create_system_configuration(obj: Dict) -> SystemConfigurationModel:
    """Creates SystemConfigurationModel object."""
    return SystemConfigurationModel.from_dict(obj)


def create_system_configuration_from_file(path: str) -> SystemConfigurationModel:
    """Creates SystemConfigurationModel object from config file."""
    return SystemConfigurationModel.from_file(path)


@pytest.mark.parametrize(
    'path', [MATCHING_MODULE_NAMES_PATH, MATCHING_ROBOT_AND_MODULE_NAMES_PATH]
)
def test_duplicate_names(path: str) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""  # noqa: E501
    with pytest.raises(DuplicateHardwareNameError) as err:
        create_system_configuration_from_file(path)
    expected_error_text = (
        "The following container names are duplicated in the "
        "configuration file: common-name"
    )
    assert err.match(expected_error_text)


def test_module_and_robot_name_the_same() -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""  # noqa: E501
    with pytest.raises(ValidationError) as err:
        create_system_configuration_from_file(INVALID_NAME_FORMAT_PATH)
    expected_error_text = ".*string does not match regex.*"
    assert err.match(expected_error_text)


@pytest.mark.parametrize(
    "path", [MODULES_ONLY_PATH, ROBOT_AND_MODULES_PATH, EMPTY_ROBOT_KEY_PATH]
)
def test_modules_exist_is_true(path: str) -> None:
    """Test that modules_exist property is true when it is supposed to be."""
    assert create_system_configuration_from_file(path).modules_exist


@pytest.mark.parametrize("path", [ROBOT_ONLY_PATH, EMPTY_MODULES_KEY_PATH])
def test_modules_exist_is_false(path: str) -> None:
    """Test that modules_exist property is false when it is supposed to be."""
    assert not create_system_configuration_from_file(path).modules_exist


@pytest.mark.parametrize(
    "path", [ROBOT_ONLY_PATH, ROBOT_AND_MODULES_PATH, EMPTY_MODULES_KEY_PATH]
)
def test_robot_exists_is_true(path: str) -> None:
    """Test that robot_exists property is true when it is supposed to be."""
    assert create_system_configuration_from_file(path).robot_exists


@pytest.mark.parametrize("path", [MODULES_ONLY_PATH, EMPTY_ROBOT_KEY_PATH])
def test_robot_exists_is_false(path: str) -> None:
    """Test that robot_exists property is false when it is supposed to be."""
    assert not create_system_configuration_from_file(path).robot_exists


def test_containers_property() -> None:
    """Test the containers property is constructed correctly."""
    containers = create_system_configuration_from_file(
        ROBOT_AND_MODULES_PATH
    ).containers
    assert set(containers.keys()) == {
        "my-robot",
        "my-heater-shaker",
        "my-heater-shaker-2",
    }
    assert isinstance(containers["my-robot"], OT2InputModel)
    assert isinstance(containers["my-heater-shaker"], HeaterShakerModuleInputModel)
    assert isinstance(containers["my-heater-shaker-2"], HeaterShakerModuleInputModel)


def test_get_by_id() -> None:
    """Test that loading containers by id works correctly."""
    system_config = create_system_configuration_from_file(ROBOT_AND_MODULES_PATH)
    assert isinstance(system_config.get_by_id("my-robot"), OT2InputModel)
    assert isinstance(
        system_config.get_by_id("my-heater-shaker"), HeaterShakerModuleInputModel
    )
    assert isinstance(
        system_config.get_by_id("my-heater-shaker-2"), HeaterShakerModuleInputModel
    )
