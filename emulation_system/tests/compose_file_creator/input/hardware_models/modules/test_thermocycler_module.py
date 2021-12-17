"""Tests for Thermocycler module."""
from typing import (
    Any,
    Dict,
)

import py
import pytest
from pydantic import parse_obj_as

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    SourceType,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    ThermocyclerModuleInputModel,
)

ID = "my-thermocycler"
HARDWARE = Hardware.THERMOCYCLER.value
EMULATION_LEVEL = EmulationLevels.HARDWARE.value
SOURCE_TYPE = SourceType.LOCAL.value


@pytest.fixture
def thermocycler_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """Thermocycler Module with default lid and plate temperature."""
    return {
        "id":                           ID,
        "hardware":                     HARDWARE,
        "emulation-level":              EMULATION_LEVEL,
        "source-type":                  SOURCE_TYPE,
        "source-location":              str(tmpdir),
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def thermocycler_set_lid_temp(thermocycler_default: Dict[str, Any]) -> Dict[str, Any]:
    """Thermocycler Module with user-specified lid temperature."""
    thermocycler_default["hardware-specific-attributes"]["lid-temperature"] = {
        "degrees-per-tick": 5.0,
        "starting":         20.0,
    }
    return thermocycler_default


@pytest.fixture
def thermocycler_set_plate_temp(
    thermocycler_set_lid_temp: Dict[str, Any]
) -> Dict[str, Any]:
    """Thermocycler Module with default lid and plate temperature."""
    thermocycler_set_lid_temp["hardware-specific-attributes"]["plate-temperature"] = {
        "degrees-per-tick": 4.5,
        "starting":         25.6,
    }
    return thermocycler_set_lid_temp


def test_default_thermocycler(thermocycler_default: Dict[str, Any]) -> None:
    """Confirm Thermocycler is parsed correctly and default lid and plate temps."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_default)
    assert therm.hardware == HARDWARE
    assert therm.id == ID
    assert therm.emulation_level == EMULATION_LEVEL
    assert therm.source_type == SOURCE_TYPE
    assert therm.hardware_specific_attributes.lid_temperature.degrees_per_tick == 2.0
    assert therm.hardware_specific_attributes.lid_temperature.starting == 23.0
    assert therm.hardware_specific_attributes.plate_temperature.degrees_per_tick == 2.0
    assert therm.hardware_specific_attributes.plate_temperature.starting == 23.0


def test_thermocycler_with_lid_temp(thermocycler_set_lid_temp: Dict[str, Any]) -> None:
    """Confirm Thermocycler is parsed correctly and user lid and default plate temps."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_set_lid_temp)
    assert therm.hardware == HARDWARE
    assert therm.id == ID
    assert therm.emulation_level == EMULATION_LEVEL
    assert therm.source_type == SOURCE_TYPE
    assert therm.hardware_specific_attributes.lid_temperature.degrees_per_tick == 5.0
    assert therm.hardware_specific_attributes.lid_temperature.starting == 20.0
    assert therm.hardware_specific_attributes.plate_temperature.degrees_per_tick == 2.0
    assert therm.hardware_specific_attributes.plate_temperature.starting == 23.0


def test_thermocycler_with_plate_temp(
    thermocycler_set_plate_temp: Dict[str, Any]
) -> None:
    """Confirm Thermocycler is parsed correctly and user lid and plate temps."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_set_plate_temp)
    assert therm.hardware == HARDWARE
    assert therm.id == ID
    assert therm.emulation_level == EMULATION_LEVEL
    assert therm.source_type == SOURCE_TYPE
    assert therm.hardware_specific_attributes.lid_temperature.degrees_per_tick == 5.0
    assert therm.hardware_specific_attributes.lid_temperature.starting == 20.0
    assert therm.hardware_specific_attributes.plate_temperature.degrees_per_tick == 4.5
    assert therm.hardware_specific_attributes.plate_temperature.starting == 25.6
