"""Tests for Thermocycler module."""
from typing import (
    Any,
    Dict,
)

import py
import pytest
from pydantic import parse_obj_as

from emulation_system.compose_file_creator.input.hardware_models import (
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceType,
)

ID = "my-thermocycler"
HARDWARE = Hardware.THERMOCYCLER_MODULE.value
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


@pytest.fixture
def hardware_emulation_level(thermocycler_default: Dict[str, Any]) -> Dict[str, Any]:
    """Return heater-shaker configuration with an invalid emulation level."""
    thermocycler_default["emulation-level"] = EmulationLevels.HARDWARE.value
    return thermocycler_default


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


def test_thermocycler_hardware_emulation_level(
    hardware_emulation_level: Dict[str, Any]
) -> None:
    """Confirm you can set Thermocycler to be emulated at the hardware level."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, hardware_emulation_level)
    assert therm.emulation_level == EmulationLevels.HARDWARE.value


def test_thermocycler_module_source_repos(
    thermocycler_default: Dict[str, Any]
) -> None:
    """Confirm that defined source repos are correct."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_default)
    assert therm.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert therm.source_repos.hardware_repo_name == OpentronsRepository.OPENTRONS_MODULES  # noqa: E501
