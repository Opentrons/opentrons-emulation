"""Tests for Thermocycler module."""
from typing import Any, Dict

import pytest
from pydantic import parse_obj_as

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    ThermocyclerModuleInputModel,
)
from tests.compose_file_creator.conftest import THERMOCYCLER_MODULE_EMULATION_LEVEL


@pytest.fixture
def thermocycler_module_set_lid_temp(
    thermocycler_model: Dict[str, Any]
) -> Dict[str, Any]:
    """Thermocycler Module with user-specified lid temperature."""
    thermocycler_model["hardware-specific-attributes"]["lid-temperature"] = {
        "degrees-per-tick": 5.0,
        "starting": 20.0,
    }
    return thermocycler_model


@pytest.fixture
def thermocycler_module_set_plate_temp(
    thermocycler_module_set_lid_temp: Dict[str, Any]
) -> Dict[str, Any]:
    """Thermocycler Module with default lid and plate temperature."""
    thermocycler_module_set_lid_temp["hardware-specific-attributes"][
        "plate-temperature"
    ] = {
        "degrees-per-tick": 4.5,
        "starting": 25.6,
    }
    return thermocycler_module_set_lid_temp


def test_default_thermocycler(thermocycler_model: Dict[str, Any]) -> None:
    """Confirm Thermocycler is parsed correctly and default lid and plate temps."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_model)
    assert therm.hardware == Hardware.THERMOCYCLER_MODULE.value
    assert therm.emulation_level == THERMOCYCLER_MODULE_EMULATION_LEVEL
    assert therm.hardware_specific_attributes.lid_temperature.degrees_per_tick == 2.0
    assert therm.hardware_specific_attributes.lid_temperature.starting == 23.0
    assert therm.hardware_specific_attributes.plate_temperature.degrees_per_tick == 2.0
    assert therm.hardware_specific_attributes.plate_temperature.starting == 23.0


def test_thermocycler_with_lid_temp(
    thermocycler_module_set_lid_temp: Dict[str, Any]
) -> None:
    """Confirm Thermocycler is parsed correctly and user lid and default plate temps."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_module_set_lid_temp)
    assert therm.hardware == Hardware.THERMOCYCLER_MODULE.value
    assert therm.emulation_level == THERMOCYCLER_MODULE_EMULATION_LEVEL
    assert therm.hardware_specific_attributes.lid_temperature.degrees_per_tick == 5.0
    assert therm.hardware_specific_attributes.lid_temperature.starting == 20.0
    assert therm.hardware_specific_attributes.plate_temperature.degrees_per_tick == 2.0
    assert therm.hardware_specific_attributes.plate_temperature.starting == 23.0


def test_thermocycler_with_plate_temp(
    thermocycler_module_set_plate_temp: Dict[str, Any]
) -> None:
    """Confirm Thermocycler is parsed correctly and user lid and plate temps."""
    therm = parse_obj_as(
        ThermocyclerModuleInputModel, thermocycler_module_set_plate_temp
    )
    assert therm.hardware == Hardware.THERMOCYCLER_MODULE.value
    assert therm.emulation_level == THERMOCYCLER_MODULE_EMULATION_LEVEL
    assert therm.hardware_specific_attributes.lid_temperature.degrees_per_tick == 5.0
    assert therm.hardware_specific_attributes.lid_temperature.starting == 20.0
    assert therm.hardware_specific_attributes.plate_temperature.degrees_per_tick == 4.5
    assert therm.hardware_specific_attributes.plate_temperature.starting == 25.6


def test_thermocycler_hardware_emulation_level(
    thermocycler_model: Dict[str, Any]
) -> None:
    """Confirm you can set Thermocycler to be emulated at the hardware level."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_model)
    assert therm.emulation_level == EmulationLevels.HARDWARE.value


def test_thermocycler_module_source_repos(thermocycler_model: Dict[str, Any]) -> None:
    """Confirm that defined source repos are correct."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_model)
    assert therm.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert (
        therm.source_repos.hardware_repo_name == OpentronsRepository.OPENTRONS_MODULES
    )
