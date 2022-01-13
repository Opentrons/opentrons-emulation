"""Tests for Thermocycler module."""
from typing import (
    Any,
    Dict,
)

from pydantic import parse_obj_as

from emulation_system.compose_file_creator.input.hardware_models import (
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
)
from tests.compose_file_creator.conftest import (
    THERMOCYCLER_MODULE_EMULATION_LEVEL,
    THERMOCYCLER_MODULE_ID,
    THREMOCYCLER_MODULE_SOURCE_TYPE,
)


def test_default_thermocycler(thermocycler_module_default: Dict[str, Any]) -> None:
    """Confirm Thermocycler is parsed correctly and default lid and plate temps."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_module_default)
    assert therm.hardware == Hardware.THERMOCYCLER_MODULE.value
    assert therm.id == THERMOCYCLER_MODULE_ID
    assert therm.emulation_level == THERMOCYCLER_MODULE_EMULATION_LEVEL
    assert therm.source_type == THREMOCYCLER_MODULE_SOURCE_TYPE
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
    assert therm.id == THERMOCYCLER_MODULE_ID
    assert therm.emulation_level == THERMOCYCLER_MODULE_EMULATION_LEVEL
    assert therm.source_type == THREMOCYCLER_MODULE_SOURCE_TYPE
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
    assert therm.id == THERMOCYCLER_MODULE_ID
    assert therm.emulation_level == THERMOCYCLER_MODULE_EMULATION_LEVEL
    assert therm.source_type == THREMOCYCLER_MODULE_SOURCE_TYPE
    assert therm.hardware_specific_attributes.lid_temperature.degrees_per_tick == 5.0
    assert therm.hardware_specific_attributes.lid_temperature.starting == 20.0
    assert therm.hardware_specific_attributes.plate_temperature.degrees_per_tick == 4.5
    assert therm.hardware_specific_attributes.plate_temperature.starting == 25.6


def test_thermocycler_hardware_emulation_level(
    thermocycler_module_hardware_emulation_level: Dict[str, Any]
) -> None:
    """Confirm you can set Thermocycler to be emulated at the hardware level."""
    therm = parse_obj_as(
        ThermocyclerModuleInputModel, thermocycler_module_hardware_emulation_level
    )
    assert therm.emulation_level == EmulationLevels.HARDWARE.value


def test_thermocycler_module_source_repos(
    thermocycler_module_default: Dict[str, Any]
) -> None:
    """Confirm that defined source repos are correct."""
    therm = parse_obj_as(ThermocyclerModuleInputModel, thermocycler_module_default)
    assert therm.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert (
        therm.source_repos.hardware_repo_name == OpentronsRepository.OPENTRONS_MODULES
    )
