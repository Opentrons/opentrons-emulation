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
                "hardware-specific-attributes": {
                    "mode": "stdin"
                }
            }
        }
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
                "hardware-specific-attributes": {
                    "mode": "stdin"
                }
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
    expected_error_text = "The following container names are duplicated in the " \
                          "configuration file: common-name"
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
