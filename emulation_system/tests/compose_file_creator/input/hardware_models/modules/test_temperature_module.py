"""Tests for Temperature Module."""
from typing import Dict, Any

import py
import pytest
from pydantic import parse_obj_as
from emulation_system.compose_file_creator.input.hardware_models import (
    TemperatureModuleModel,
)
from emulation_system.compose_file_creator.config_file_settings import (
    Hardware,
    EmulationLevel,
    SourceType,
)

ID = "my-temperature"
HARDWARE = Hardware.TEMPERATURE.value
EMULATION_LEVEL = EmulationLevel.FIRMWARE.value
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


def test_default_temperature_module(temperature_module_default: Dict[str, Any]) -> None:
    """Confirm Temperature Module is parsed correctly and defaults are applied."""
    therm = parse_obj_as(TemperatureModuleModel, temperature_module_default)
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
    therm = parse_obj_as(TemperatureModuleModel, temperature_module_set_temp)
    assert therm.hardware == HARDWARE
    assert therm.id == ID
    assert therm.emulation_level == EMULATION_LEVEL
    assert therm.source_type == SOURCE_TYPE
    assert therm.hardware_specific_attributes.temperature.degrees_per_tick == 5.0
    assert therm.hardware_specific_attributes.temperature.starting == 20.0
