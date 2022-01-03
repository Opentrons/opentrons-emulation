"""Tests for Temperature Module."""
from typing import (
    Any,
    Dict,
)

import py
import pytest
from pydantic import (
    ValidationError,
    parse_obj_as,
)

from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    TemperatureModuleInputModel,
)

ID = "my-temperature"
HARDWARE = Hardware.TEMPERATURE_MODULE.value
EMULATION_LEVEL = EmulationLevels.FIRMWARE.value
SOURCE_TYPE = SourceType.LOCAL.value


@pytest.fixture
def temperature_module_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """Temperature Module with default temperature settings specified."""
    return {
        "id": ID,
        "hardware": HARDWARE,
        "emulation-level": EMULATION_LEVEL,
        "source-type": SOURCE_TYPE,
        "source-location": str(tmpdir),
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def temperature_module_set_temp(
    temperature_module_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Temperature module with user-specified temperature settings."""
    temperature_module_default["hardware-specific-attributes"]["temperature"] = {
        "degrees-per-tick": 5.0,
        "starting": 20.0,
    }
    return temperature_module_default


@pytest.fixture
def bad_emulation_level(temperature_module_default: Dict[str, Any]) -> Dict[str, Any]:
    """Return temperature module configuration with an invalid emulation level."""
    temperature_module_default["emulation-level"] = EmulationLevels.HARDWARE.value
    return temperature_module_default


def test_default_temperature_module(temperature_module_default: Dict[str, Any]) -> None:
    """Confirm Temperature Module is parsed correctly and defaults are applied."""
    therm = parse_obj_as(TemperatureModuleInputModel, temperature_module_default)
    assert therm.hardware == HARDWARE
    assert therm.id == ID
    assert therm.emulation_level == EMULATION_LEVEL
    assert therm.source_type == SOURCE_TYPE
    assert therm.hardware_specific_attributes.temperature.degrees_per_tick == 2.0
    assert therm.hardware_specific_attributes.temperature.starting == 23.0


def test_temperature_module_with_temp(
    temperature_module_set_temp: Dict[str, Any]
) -> None:
    """Confirm Temperature Module is parsed correctly.

    Confirm user-defined settings are applied.
    """
    therm = parse_obj_as(TemperatureModuleInputModel, temperature_module_set_temp)
    assert therm.hardware == HARDWARE
    assert therm.id == ID
    assert therm.emulation_level == EMULATION_LEVEL
    assert therm.source_type == SOURCE_TYPE
    assert therm.hardware_specific_attributes.temperature.degrees_per_tick == 5.0
    assert therm.hardware_specific_attributes.temperature.starting == 20.0


def test_temperature_module_with_bad_emulation_level(
    bad_emulation_level: Dict[str, Any]
) -> None:
    """Confirm that there is a validation error when a bad emulation level is passed."""
    with pytest.raises(ValidationError):
        parse_obj_as(TemperatureModuleInputModel, bad_emulation_level)


def test_temperature_module_source_repos(
    temperature_module_default: Dict[str, Any]
) -> None:
    """Confirm that defined source repos are correct."""
    temp = parse_obj_as(TemperatureModuleInputModel, temperature_module_default)
    assert temp.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert temp.source_repos.hardware_repo_name is None
