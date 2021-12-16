"""Tests for Magenetic Module."""
from typing import Dict, Any

import py
import pytest
from pydantic import parse_obj_as
from emulation_system.compose_file_creator.input.hardware_models import (
    MagneticModuleInputModel,
)
from emulation_system.compose_file_creator.config_file_settings import (
    Hardware,
    EmulationLevel,
    SourceType,
)

ID = "my-magnetic"
HARDWARE = Hardware.MAGNETEIC.value
EMULATION_LEVEL = EmulationLevel.FIRMWARE.value
SOURCE_TYPE = SourceType.LOCAL.value


@pytest.fixture
def magnetic_module_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """Magnetic Module. Does not contain any hardware-specific-attributes."""
    return {
        "id": ID,
        "hardware": HARDWARE,
        "emulation-level": EMULATION_LEVEL,
        "source-type": SOURCE_TYPE,
        "source-location": str(tmpdir),
        "hardware-specific-attributes": {},
    }


def test_default_magnetic_module(magnetic_module_default: Dict[str, Any]) -> None:
    """Confirm Magnetic Module is parsed correctly."""
    mag = parse_obj_as(MagneticModuleInputModel, magnetic_module_default)
    assert mag.hardware == HARDWARE
    assert mag.id == ID
    assert mag.emulation_level == EMULATION_LEVEL
    assert mag.source_type == SOURCE_TYPE
