"""Conftest for compose_file_creator package."""
from typing import Any, Dict

import py
import pytest

from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    SourceType,
)

HEATER_SHAKER_MODULE_ID = "shakey-and-warm"
MAGNETIC_MODULE_ID = "fatal-attraction"
TEMPERATURE_MODULE_ID = "temperamental"
THERMOCYCLER_MODULE_ID = "t00-hot-to-handle"
OT2_ID = "brobot"
OT3_ID = "edgar-allen-poebot"
EMULATOR_PROXY_ID = "emulator-proxy"
SMOOTHIE_ID = "smoothie"

HEATER_SHAKER_MODULE_EMULATION_LEVEL = EmulationLevels.HARDWARE.value
MAGNETIC_MODULE_EMULATION_LEVEL = EmulationLevels.FIRMWARE.value
TEMPERATURE_MODULE_EMULATION_LEVEL = EmulationLevels.FIRMWARE.value
THERMOCYCLER_MODULE_EMULATION_LEVEL = EmulationLevels.HARDWARE.value
OT2_EMULATION_LEVEL = EmulationLevels.FIRMWARE.value
OT3_EMULATION_LEVEL = EmulationLevels.HARDWARE.value

HEATER_SHAKER_MODULE_SOURCE_TYPE = SourceType.REMOTE.value
MAGNETIC_MODULE_SOURCE_TYPE = SourceType.LOCAL.value
TEMPERATURE_MODULE_SOURCE_TYPE = SourceType.LOCAL.value
THERMOCYCLER_MODULE_SOURCE_TYPE = SourceType.LOCAL.value
OT2_SOURCE_TYPE = SourceType.LOCAL.value
OT3_SOURCE_TYPE = SourceType.LOCAL.value

SYSTEM_UNIQUE_ID = "testing-1-2-3"


@pytest.fixture
def opentrons_dir(tmpdir: py.path.local) -> str:
    """Get path to temporary opentrons directory.

    Note that this variable is scoped to the test. So if you call the fixture from
    different places in the test the variable will be the same.
    """
    return str(tmpdir.mkdir("opentrons"))


@pytest.fixture
def opentrons_modules_dir(tmpdir: py.path.local) -> str:
    """Get path to temporary opentrons-modules directory.

    Note that this variable is scoped to the test. So if you call the fixture from
    different places in the test the variable will be the same.
    """
    return str(tmpdir.mkdir("opentrons-modules"))


@pytest.fixture
def heater_shaker_module_default(opentrons_modules_dir: str) -> Dict[str, Any]:
    """Return heater-shaker configuration dictionary."""
    return {
        "id": HEATER_SHAKER_MODULE_ID,
        "hardware": Hardware.HEATER_SHAKER_MODULE.value,
        "emulation-level": HEATER_SHAKER_MODULE_EMULATION_LEVEL,
        "source-type": HEATER_SHAKER_MODULE_SOURCE_TYPE,
        "source-location": "latest",
    }


@pytest.fixture
def magnetic_module_default(opentrons_dir: str) -> Dict[str, Any]:
    """Magnetic Module. Does not contain any hardware-specific-attributes."""
    return {
        "id": MAGNETIC_MODULE_ID,
        "hardware": Hardware.MAGNETIC_MODULE.value,
        "emulation-level": MAGNETIC_MODULE_EMULATION_LEVEL,
        "source-type": MAGNETIC_MODULE_SOURCE_TYPE,
        "source-location": opentrons_dir,
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def temperature_module_default(opentrons_dir: str) -> Dict[str, Any]:
    """Temperature Module with default temperature settings specified."""
    return {
        "id": TEMPERATURE_MODULE_ID,
        "hardware": Hardware.TEMPERATURE_MODULE.value,
        "emulation-level": TEMPERATURE_MODULE_EMULATION_LEVEL,
        "source-type": TEMPERATURE_MODULE_SOURCE_TYPE,
        "source-location": opentrons_dir,
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def thermocycler_module_default(opentrons_modules_dir: str) -> Dict[str, Any]:
    """Thermocycler Module with default lid and plate temperature."""
    return {
        "id": THERMOCYCLER_MODULE_ID,
        "hardware": Hardware.THERMOCYCLER_MODULE.value,
        "emulation-level": THERMOCYCLER_MODULE_EMULATION_LEVEL,
        "source-type": THERMOCYCLER_MODULE_SOURCE_TYPE,
        "source-location": opentrons_modules_dir,
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def ot2_default(opentrons_dir: str) -> Dict[str, Any]:
    """OT-2 using default pipettes."""
    return {
        "id": OT2_ID,
        "hardware": Hardware.OT2.value,
        "emulation-level": OT2_EMULATION_LEVEL,
        "source-type": OT2_SOURCE_TYPE,
        "source-location": opentrons_dir,
        "robot-server-source-type": "local",
        "robot-server-source-location": opentrons_dir,
        "exposed-port": 5000,
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def ot3_default(opentrons_dir: str) -> Dict[str, Any]:
    """OT-3 using default pipettes."""
    return {
        "id": OT3_ID,
        "hardware": Hardware.OT3.value,
        "emulation-level": OT3_EMULATION_LEVEL,
        "source-type": OT3_SOURCE_TYPE,
        "source-location": opentrons_dir,
        "robot-server-source-type": "remote",
        "robot-server-source-location": "latest",
        "exposed-port": 5000,
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def ot2_only(ot2_default: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with OT-2 only."""
    return {"robot": ot2_default}


@pytest.fixture
def ot3_only(ot3_default: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with OT-3 only."""
    return {"robot": ot3_default}


@pytest.fixture
def modules_only(
    thermocycler_module_default: Dict[str, Any],
    temperature_module_default: Dict[str, Any],
    magnetic_module_default: Dict[str, Any],
    heater_shaker_module_default: Dict[str, Any],
) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with modules only."""
    return {
        "modules": [
            thermocycler_module_default,
            temperature_module_default,
            magnetic_module_default,
            heater_shaker_module_default,
        ]
    }


@pytest.fixture
def ot2_and_modules(
    modules_only: Dict[str, Any], ot2_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot and modules."""
    modules_only["robot"] = ot2_default
    return modules_only


@pytest.fixture
def ot3_and_modules(
    modules_only: Dict[str, Any], ot3_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot and modules."""
    modules_only["robot"] = ot3_default
    return modules_only


@pytest.fixture
def with_system_unique_id(ot2_and_modules: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and system-unique-id."""  # noqa: E501
    ot2_and_modules["system-unique-id"] = SYSTEM_UNIQUE_ID
    return ot2_and_modules
