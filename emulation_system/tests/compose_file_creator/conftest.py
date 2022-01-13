"""Conftest for compose_file_creator package."""

from typing import (
    Any,
    Dict,
)

import py
import pytest

from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    HeaterShakerModes,
    SourceType,
)

HEATER_SHAKER_MODULE_ID = "my-heater-shaker"
MAGNETIC_MODULE_ID = "my-magnetic"
TEMPERATURE_MODULE_ID = "my-temperature"
THERMOCYCLER_MODULE_ID = "my-thermocycler"


HEATER_SHAKER_MODULE_EMULATION_LEVEL = EmulationLevels.HARDWARE.value
MAGNETIC_MODULE_EMULATION_LEVEL = EmulationLevels.FIRMWARE.value
TEMPERATURE_MODULE_EMULATION_LEVEL = EmulationLevels.FIRMWARE.value
THERMOCYCLER_MODULE_EMULATION_LEVEL = EmulationLevels.HARDWARE.value


HEATER_SHAKER_MODULE_SOURCE_TYPE = SourceType.LOCAL.value
MAGNETIC_MODULE_SOURCE_TYPE = SourceType.LOCAL.value
TEMPERATURE_MODULE_SOURCE_TYPE = SourceType.LOCAL.value
THREMOCYCLER_MODULE_SOURCE_TYPE = SourceType.LOCAL.value


@pytest.fixture
def heater_shaker_module_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """Return heater-shaker configuration dictionary."""
    return {
        "id": HEATER_SHAKER_MODULE_ID,
        "hardware": Hardware.HEATER_SHAKER_MODULE.value,
        "emulation-level": HEATER_SHAKER_MODULE_EMULATION_LEVEL,
        "source-type": HEATER_SHAKER_MODULE_SOURCE_TYPE,
        "source-location": str(tmpdir),
    }


@pytest.fixture
def heater_shaker_module_bad_emulation_level(
    heater_shaker_module_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Return heater-shaker configuration with an invalid emulation level."""
    heater_shaker_module_default["emulation-level"] = EmulationLevels.FIRMWARE.value
    return heater_shaker_module_default


@pytest.fixture
def heater_shaker_module_use_stdin(
    heater_shaker_module_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Heater-shaker dictionary with mode set to stdin."""
    heater_shaker_module_default["hardware_specific_attributes"] = {
        "mode": HeaterShakerModes.STDIN
    }
    return heater_shaker_module_default


@pytest.fixture
def magnetic_module_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """Magnetic Module. Does not contain any hardware-specific-attributes."""
    return {
        "id": MAGNETIC_MODULE_ID,
        "hardware": Hardware.MAGNETIC_MODULE.value,
        "emulation-level": MAGNETIC_MODULE_EMULATION_LEVEL,
        "source-type": MAGNETIC_MODULE_SOURCE_TYPE,
        "source-location": str(tmpdir),
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def magnetic_module_bad_emulation_level(
    magnetic_module_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Return magnetic module configuration with an invalid emulation level."""
    magnetic_module_default["emulation-level"] = EmulationLevels.HARDWARE.value
    return magnetic_module_default


@pytest.fixture
def temperature_module_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """Temperature Module with default temperature settings specified."""
    return {
        "id": TEMPERATURE_MODULE_ID,
        "hardware": Hardware.TEMPERATURE_MODULE.value,
        "emulation-level": TEMPERATURE_MODULE_EMULATION_LEVEL,
        "source-type": TEMPERATURE_MODULE_SOURCE_TYPE,
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
def temperature_module_bad_emulation_level(
    temperature_module_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Return temperature module configuration with an invalid emulation level."""
    temperature_module_default["emulation-level"] = EmulationLevels.HARDWARE.value
    return temperature_module_default


@pytest.fixture
def thermocycler_module_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """Thermocycler Module with default lid and plate temperature."""
    return {
        "id": THERMOCYCLER_MODULE_ID,
        "hardware": Hardware.THERMOCYCLER_MODULE.value,
        "emulation-level": THERMOCYCLER_MODULE_EMULATION_LEVEL,
        "source-type": THREMOCYCLER_MODULE_SOURCE_TYPE,
        "source-location": str(tmpdir),
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def thermocycler_module_set_lid_temp(
    thermocycler_module_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Thermocycler Module with user-specified lid temperature."""
    thermocycler_module_default["hardware-specific-attributes"]["lid-temperature"] = {
        "degrees-per-tick": 5.0,
        "starting": 20.0,
    }
    return thermocycler_module_default


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


@pytest.fixture
def thermocycler_module_hardware_emulation_level(
    thermocycler_module_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Return heater-shaker configuration with an invalid emulation level."""
    thermocycler_module_default["emulation-level"] = EmulationLevels.HARDWARE.value
    return thermocycler_module_default
