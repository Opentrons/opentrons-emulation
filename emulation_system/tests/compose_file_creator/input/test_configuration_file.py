"""Tests for SystemConfigurationModel class.

Note: Do not need to test matching module names because module names cannot be the same
by definition of dict.
"""
from typing import Dict

import pytest
from pydantic import ValidationError

from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)


@pytest.fixture
def matching_robot_and_module_names() -> Dict:
    """Configuration file with matching robot and module name."""
    return {
        "robot":   {
            "common-name": {
                "hardware":        "ot2",
                "emulation-level": "firmware",
                "source-type":     "remote",
                "source-location": "latest",
            }
        },
        "modules": {
            "common-name": {
                "hardware":                     "heater-shaker-module",
                "emulation-level":              "hardware",
                "source-type":                  "remote",
                "source-location":              "latest",
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
                "hardware":                     "heater-shaker-module",
                "emulation-level":              "hardware",
                "source-type":                  "remote",
                "source-location":              "latest",
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
                "hardware":        "ot2",
                "emulation-level": "firmware",
                "source-type":     "remote",
                "source-location": "latest",
            },
            "robot-2": {
                "hardware":        "ot2",
                "emulation-level": "firmware",
                "source-type":     "remote",
                "source-location": "latest",
            },
        }
    }


@pytest.fixture
def modules_only() -> Dict:
    """Configuration with only modules."""
    return {
        "modules": {
            "my-heater-shaker":   {
                "hardware":                     "heater-shaker-module",
                "emulation-level":              "hardware",
                "source-type":                  "remote",
                "source-location":              "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            },
            "my-heater-shaker-2": {
                "hardware":                     "heater-shaker-module",
                "emulation-level":              "hardware",
                "source-type":                  "remote",
                "source-location":              "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            }
        }
    }


@pytest.fixture
def robot_only() -> Dict:
    """Configuration with only modules."""
    return {
        "robot": {
            "my-robot": {
                "hardware":        "ot2",
                "emulation-level": "firmware",
                "source-type":     "remote",
                "source-location": "latest",
            }
        }
    }


@pytest.fixture
def robot_and_modules() -> Dict:
    """Configuration with robot and modules."""
    return {
        "robot":   {
            "my-robot": {
                "hardware":        "ot2",
                "emulation-level": "firmware",
                "source-type":     "remote",
                "source-location": "latest",
            }
        },
        "modules": {
            "my-heater-shaker":   {
                "hardware":                     "heater-shaker-module",
                "emulation-level":              "hardware",
                "source-type":                  "remote",
                "source-location":              "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            },
            "my-heater-shaker-2": {
                "hardware":                     "heater-shaker-module",
                "emulation-level":              "hardware",
                "source-type":                  "remote",
                "source-location":              "latest",
                "hardware-specific-attributes": {"mode": "stdin"},
            }
        }
    }


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
    "config_dict", [
        pytest.lazy_fixture("modules_only"),
        pytest.lazy_fixture("robot_and_modules"),
    ]
    )
def test_modules_exist_is_true(config_dict: Dict) -> None:
    """Test that modules_exist property is true when it is supposed to be."""
    assert create_system_configuration(config_dict).modules_exist


def test_modules_exist_is_false(robot_only: Dict) -> None:
    """Test that modules_exist property is false when it is supposed to be."""
    assert not create_system_configuration(robot_only).modules_exist


@pytest.mark.parametrize(
    "config_dict", [
        pytest.lazy_fixture("robot_only"),
        pytest.lazy_fixture("robot_and_modules"),
    ]
    )
def test_robot_exists_is_true(config_dict: Dict) -> None:
    """Test that robot_exists property is true when it is supposed to be."""
    assert create_system_configuration(config_dict).robot_exists


def test_robot_exists_is_false(modules_only: Dict) -> None:
    """Test that robot_exists property is false when it is supposed to be."""
    assert not create_system_configuration(modules_only ).robot_exists
