"""Conftest for compose_file_creator package."""
import pathlib
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

HEATER_SHAKER_MODULE_ID = "shakey-and-warm"
MAGNETIC_MODULE_ID = "fatal-attraction"
TEMPERATURE_MODULE_ID = "temperamental"
THERMOCYCLER_MODULE_ID = "t00-hot-to-handle"
OT2_ID = "brobot"
OT3_ID = "edgar-allen-poebot"
EMULATOR_PROXY_ID = "emulator-proxy"

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
        "source-location": opentrons_modules_dir,
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
def magnetic_module_bad_emulation_level(
    magnetic_module_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Return magnetic module configuration with an invalid emulation level."""
    magnetic_module_default["emulation-level"] = EmulationLevels.HARDWARE.value
    return magnetic_module_default


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


@pytest.fixture
def ot2_default(opentrons_dir: str) -> Dict[str, Any]:
    """OT-2 using default pipettes."""
    return {
        "id": OT2_ID,
        "hardware": Hardware.OT2.value,
        "emulation-level": OT2_EMULATION_LEVEL,
        "source-type": OT2_SOURCE_TYPE,
        "source-location": opentrons_dir,
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
        "exposed-port": 5000,
        "hardware-specific-attributes": {},
    }


@pytest.fixture
def ot2_with_overridden_bound_port(ot2_default: Dict[str, Any]) -> Dict[str, Any]:
    """OT-2 with overridden bound-port."""
    ot2_default["bound-port"] = 2500
    return ot2_default


@pytest.fixture
def ot2_bad_emulation_level(ot2_default: Dict[str, Any]) -> Dict[str, Any]:
    """Return magnetic module configuration with an invalid emulation level."""
    ot2_default["emulation-level"] = EmulationLevels.HARDWARE.value
    return ot2_default


@pytest.fixture
def ot2_with_pipettes(ot2_default: Dict[str, Any]) -> Dict[str, Any]:
    """OT-2 using user-specified pipettes."""
    ot2_default["hardware-specific-attributes"]["left-pipette"] = {}
    ot2_default["hardware-specific-attributes"]["left-pipette"]["model"] = "test_1"
    ot2_default["hardware-specific-attributes"]["left-pipette"]["id"] = "test_1_id"

    ot2_default["hardware-specific-attributes"]["right-pipette"] = {}
    ot2_default["hardware-specific-attributes"]["right-pipette"]["model"] = "test_2"
    ot2_default["hardware-specific-attributes"]["right-pipette"]["id"] = "test_2_id"
    return ot2_default


@pytest.fixture
def ot2_with_mounts(tmp_path: pathlib.Path, ot2_default: Dict) -> Dict:
    """Configuration of a robot with extra bind mounts."""
    datadog_dir = tmp_path / "Datadog"
    datadog_dir.mkdir()
    datadog_file = datadog_dir / "log.txt"
    datadog_file.write_text("test")

    log_dir = tmp_path / "Log"
    log_dir.mkdir()

    ot2_default["robot"][OT2_ID]["extra-mounts"] = [
        {
            "name": "DATADOG",
            "source-path": str(datadog_file),
            "mount-path": "/datadog/log.txt",
            "type": "file",
        },
        {
            "name": "LOG_FILES",
            "source-path": str(log_dir),
            "mount-path": "/var/log/opentrons/",
            "type": "directory",
        },
    ]
    return ot2_default


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
def robot_and_modules(
    modules_only: Dict[str, Any], ot2_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot and modules."""
    modules_only["robot"] = ot2_default
    return modules_only


@pytest.fixture
def with_system_unique_id(robot_and_modules: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and system-unique-id."""  # noqa: E501
    robot_and_modules["system-unique-id"] = SYSTEM_UNIQUE_ID
    return robot_and_modules
