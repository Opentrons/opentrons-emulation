"""Tests for heater-shaker module."""
from typing import Dict, Any

import py.path
import pytest
from pydantic import parse_obj_as
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
)
from emulation_system.compose_file_creator.config_file_settings import (
    HeaterShakerModes,
    Hardware,
    EmulationLevels,
    SourceType,
)

ID = "my-heater-shaker"
HARDWARE = Hardware.HEATER_SHAKER_MODULE.value
EMULATION_LEVEL = EmulationLevels.HARDWARE.value
SOURCE_TYPE = SourceType.LOCAL.value


@pytest.fixture
def heater_shaker_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """Return heater-shaker configuration dictionary."""
    return {
        "id": ID,
        "hardware": HARDWARE,
        "emulation-level": EMULATION_LEVEL,
        "source-type": SOURCE_TYPE,
        "source-location": str(tmpdir),
    }


@pytest.fixture
def heater_shaker_use_stdin(heater_shaker_default: Dict[str, Any]) -> Dict[str, Any]:
    """Heater-shaker dictionary with mode set to stdin."""
    heater_shaker_default["hardware_specific_attributes"] = {}
    heater_shaker_default["hardware_specific_attributes"][
        "mode"
    ] = HeaterShakerModes.STDIN
    return heater_shaker_default


def test_default_heater_shaker(heater_shaker_default: Dict[str, Any]) -> None:
    """Confirm Heater-Shaker is parsed right and default mode of socket is set."""
    hs = parse_obj_as(HeaterShakerModuleInputModel, heater_shaker_default)
    assert hs.hardware == HARDWARE
    assert hs.id == ID
    assert hs.emulation_level == EMULATION_LEVEL
    assert hs.source_type == SOURCE_TYPE
    assert hs.hardware_specific_attributes.mode == HeaterShakerModes.SOCKET


def test_heater_shaker_with_stdin(heater_shaker_use_stdin: Dict[str, Any]) -> None:
    """Confirm Heater-Shaker is parsed right and stdin mode is picked up."""
    hs = parse_obj_as(HeaterShakerModuleInputModel, heater_shaker_use_stdin)
    assert hs.hardware == HARDWARE
    assert hs.id == ID
    assert hs.emulation_level == EMULATION_LEVEL
    assert hs.source_type == SOURCE_TYPE
    assert hs.hardware_specific_attributes.mode == HeaterShakerModes.STDIN
