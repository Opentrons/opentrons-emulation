"""Tests for SystemConfigurationModel class.

Note: Do not need to test matching module names because module names cannot be the same
by definition of dict.
"""
import json
import pathlib
from typing import Dict

import pytest
from pydantic import ValidationError
from pytest_lazyfixture import lazy_fixture  # type: ignore
from pydantic import ValidationError
from pytest_lazyfixture import lazy_fixture  # type: ignore

from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    OT2InputModel,
)
from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    NoMountsDefinedException,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DirectoryExtraMount,
    FileExtraMount,
)


@pytest.fixture
def matching_robot_and_module_names() -> Dict:
    """Configuration file with matching robot and module name."""
    return {
        "robot": {
            "common-name": {
                "hardware": "ot2",
                "emulation-level": "firmware",
                "source-type": "remote",
                "source-location": "latest",
            }
        },
        "modules": {
            "common-name": {
                "hardware": "heater-shaker-module",
                "emulation-level": "hardware",
                "source-type": "remote",
                "source-location": "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            }
        },
    }


@pytest.fixture
def invalid_name_format() -> Dict:
    """Configuration file with matching robot and module name."""
    return {
        "modules": {
            "invalid name with spaces": {
                "hardware": "heater-shaker-module",
                "emulation-level": "hardware",
                "source-type": "remote",
                "source-location": "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            }
        }
    }


@pytest.fixture
def multiple_robots() -> Dict:
    """Configuration file with matching robot and module name."""
    return {
        "robot": {
            "robot-1": {
                "hardware": "ot2",
                "emulation-level": "firmware",
                "source-type": "remote",
                "source-location": "latest",
            },
            "robot-2": {
                "hardware": "ot2",
                "emulation-level": "firmware",
                "source-type": "remote",
                "source-location": "latest",
            },
        }
    }


@pytest.fixture
def modules_only() -> Dict:
    """Configuration with only modules."""
    return {
        "modules": {
            "my-heater-shaker": {
                "hardware": "heater-shaker-module",
                "emulation-level": "hardware",
                "source-type": "remote",
                "source-location": "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            },
            "my-heater-shaker-2": {
                "hardware": "heater-shaker-module",
                "emulation-level": "hardware",
                "source-type": "remote",
                "source-location": "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            },
        }
    }


@pytest.fixture
def robot_only() -> Dict:
    """Configuration with only modules."""
    return {
        "robot": {
            "my-robot": {
                "hardware": "ot2",
                "emulation-level": "firmware",
                "source-type": "remote",
                "source-location": "latest",
            }
        }
    }


@pytest.fixture
def robot_and_modules() -> Dict:
    """Configuration with robot and modules."""
    return {
        "robot": {
            "my-robot": {
                "hardware": "ot2",
                "emulation-level": "firmware",
                "source-type": "remote",
                "source-location": "latest",
            }
        },
        "modules": {
            "my-heater-shaker": {
                "hardware": "heater-shaker-module",
                "emulation-level": "hardware",
                "source-type": "remote",
                "source-location": "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            },
            "my-heater-shaker-2": {
                "hardware": "heater-shaker-module",
                "emulation-level": "hardware",
                "source-type": "remote",
                "source-location": "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            },
        },
    }


@pytest.fixture
def extra_mounts(tmp_path: pathlib.Path, robot_only: Dict) -> Dict:
    """Configuration of a robot with extra bind mounts."""
    datadog_dir = tmp_path / "Datadog"
    datadog_dir.mkdir()
    datadog_file = datadog_dir / "log.txt"
    datadog_file.write_text("test")

    log_dir = tmp_path / "Log"
    log_dir.mkdir()

    robot_only["robot"]["my-robot"]["extra-mounts"] = {
        "DATADOG": {
            "source-path": str(datadog_file),
            "mount-path": "/datadog/log.txt",
            "type": "file",
        },
        "LOG_FILES": {
            "source-path": str(log_dir),
            "mount-path": "/var/log/opentrons/",
            "type": "directory",
        },
    }
    return robot_only


@pytest.fixture
def invalid_mount_name(extra_mounts: Dict) -> Dict:
    """Configuration with an invalid mount name."""
    extra_mounts['robot']['my-robot']['extra-mounts']['data-dog'] = extra_mounts['robot']['my-robot']['extra-mounts']['DATADOG']  # noqa: E501
    del extra_mounts['robot']['my-robot']['extra-mounts']['DATADOG']
    return extra_mounts


@pytest.fixture
def config_from_json(
    tmp_path: pathlib.Path, robot_and_modules: Dict
) -> SystemConfigurationModel:
    """Create SystemConfigurationModel from a JSON file."""
    p = tmp_path / "temp.json"
    file = open(p, "w")
    json.dump(robot_and_modules, file, indent=4)
    file.close()
    return SystemConfigurationModel.from_file(str(p))


def create_system_configuration(obj: Dict) -> SystemConfigurationModel:
    """Creates SystemConfigurationModel object."""
    return SystemConfigurationModel.from_dict(obj)


def test_invalid_name_format(matching_robot_and_module_names: Dict) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""  # noqa: E501
    with pytest.raises(ValidationError) as err:
        create_system_configuration(matching_robot_and_module_names)
    expected_error_text = (
        "The following container names are duplicated in the "
        "configuration file: common-name"
    )
    assert err.match(expected_error_text)


def test_module_and_robot_name_the_same(invalid_name_format: Dict) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""  # noqa: E501
    with pytest.raises(ValidationError) as err:
        create_system_configuration(invalid_name_format)
    expected_error_text = ".*invalid name with spaces.*"
    assert err.match(expected_error_text)


def test_multiple_robots(multiple_robots: Dict) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""  # noqa: E501
    with pytest.raises(ValidationError) as err:
        create_system_configuration(multiple_robots)
    expected_error_text = "You can only define 1 robot"
    assert err.match(expected_error_text)


@pytest.mark.parametrize(
    "config_dict",
    [
        lazy_fixture("modules_only"),
        lazy_fixture("robot_and_modules"),
    ],
)
def test_modules_exist_is_true(config_dict: Dict) -> None:
    """Test that modules_exist property is true when it is supposed to be."""
    assert create_system_configuration(config_dict).modules_exist


def test_modules_exist_is_false(robot_only: Dict) -> None:
    """Test that modules_exist property is false when it is supposed to be."""
    assert not create_system_configuration(robot_only).modules_exist


@pytest.mark.parametrize(
    "config_dict",
    [
        lazy_fixture("robot_only"),
        lazy_fixture("robot_and_modules"),
    ],
)
def test_robot_exists_is_true(config_dict: Dict) -> None:
    """Test that robot_exists property is true when it is supposed to be."""
    assert create_system_configuration(config_dict).robot_exists


def test_robot_exists_is_false(modules_only: Dict) -> None:
    """Test that robot_exists property is false when it is supposed to be."""
    assert not create_system_configuration(modules_only).robot_exists


def test_containers_property(robot_and_modules: Dict) -> None:
    """Test the containers property is constructed correctly."""
    containers = create_system_configuration(robot_and_modules).containers
    assert set(containers.keys()) == {
        "my-robot",
        "my-heater-shaker",
        "my-heater-shaker-2",
    }
    assert isinstance(containers["my-robot"], OT2InputModel)
    assert isinstance(containers["my-heater-shaker"], HeaterShakerModuleInputModel)
    assert isinstance(containers["my-heater-shaker-2"], HeaterShakerModuleInputModel)


def test_get_by_id(robot_and_modules: Dict) -> None:
    """Test that loading containers by id works correctly."""
    system_config = create_system_configuration(robot_and_modules)
    assert isinstance(system_config.get_by_id("my-robot"), OT2InputModel)
    assert isinstance(
        system_config.get_by_id("my-heater-shaker"), HeaterShakerModuleInputModel
    )
    assert isinstance(
        system_config.get_by_id("my-heater-shaker-2"), HeaterShakerModuleInputModel
    )


def test_from_file(config_from_json: SystemConfigurationModel) -> None:
    """Test that parsing a config from a JSON file works correctly."""
    assert isinstance(config_from_json.get_by_id("my-robot"), OT2InputModel)
    assert isinstance(
        config_from_json.get_by_id("my-heater-shaker"), HeaterShakerModuleInputModel
    )
    assert isinstance(
        config_from_json.get_by_id("my-heater-shaker-2"), HeaterShakerModuleInputModel
    )


def test_extra_mounts(extra_mounts: Dict) -> None:
    """Test that extra mounts are created correctly."""
    robot = create_system_configuration(extra_mounts).get_robot()
    datadog_mount = robot.get_mount_by_name("DATADOG")
    assert isinstance(datadog_mount, FileExtraMount)
    assert datadog_mount.name == "DATADOG"
    assert datadog_mount.mount_path == "/datadog/log.txt"

    log_mount = robot.get_mount_by_name("LOG_FILES")
    assert isinstance(log_mount, DirectoryExtraMount)
    assert log_mount.name == "LOG_FILES"
    assert log_mount.mount_path == "/var/log/opentrons/"


def test_loading_mount_when_none_exist(robot_only: Dict) -> None:
    """Test NoMountsDefinedException is thrown when you load a nonexistent mount."""
    robot = create_system_configuration(robot_only).get_robot()
    with pytest.raises(NoMountsDefinedException) as err:
        robot.get_mount_by_name("ugh")
    expected_error_text = "You have no mounts defined."
    assert err.match(expected_error_text)


def test_invalid_mount_name(invalid_mount_name: Dict) -> None:
    """Test that ValidationError is thrown when you have an invalid mount name."""
    with pytest.raises(ValidationError):
        create_system_configuration(invalid_mount_name)
