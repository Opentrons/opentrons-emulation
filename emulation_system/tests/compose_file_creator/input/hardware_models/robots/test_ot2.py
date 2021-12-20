"""Tests for OT-2 robot."""
from typing import Dict, Any

import py
import pytest
from pydantic import parse_obj_as
from emulation_system.compose_file_creator.input.hardware_models import OT2Model
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    EmulationLevels,
    SourceType,
)

ID = "my-ot2"
HARDWARE = Hardware.OT2.value
EMULATION_LEVEL = EmulationLevels.FIRMWARE.value
SOURCE_TYPE = SourceType.LOCAL.value


@pytest.fixture
def ot2_default(tmpdir: py.path.local) -> Dict[str, Any]:
    """OT-2 using default pipettes."""
    return {
        "id": ID,
        "hardware": HARDWARE,
        "emulation-level": EMULATION_LEVEL,
        "source-type": SOURCE_TYPE,
        "source-location": str(tmpdir),
        "hardware-specific-attributes": {},
    }


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


def test_default_ot2(ot2_default: Dict[str, Any]) -> None:
    """Confirm OT-2 is parsed correctly and default pipettes are applied."""
    ot2 = parse_obj_as(OT2Model, ot2_default)
    assert ot2.hardware == HARDWARE
    assert ot2.id == ID
    assert ot2.emulation_level == EMULATION_LEVEL
    assert ot2.source_type == SOURCE_TYPE
    assert ot2.hardware_specific_attributes.left_pipette.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.left_pipette.id == "P20SV202020070101"
    assert ot2.hardware_specific_attributes.right_pipette.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.right_pipette.id == "P20SV202020070101"


def test_ot2_with_custom_pipettes(ot2_with_pipettes: Dict[str, Any]) -> None:
    """Confirm OT-2 is parsed correctly and user-defined pipettes are applied."""
    ot2 = parse_obj_as(OT2Model, ot2_with_pipettes)
    assert ot2.hardware == HARDWARE
    assert ot2.id == ID
    assert ot2.emulation_level == EMULATION_LEVEL
    assert ot2.source_type == SOURCE_TYPE
    assert ot2.hardware_specific_attributes.left_pipette.model == "test_1"
    assert ot2.hardware_specific_attributes.left_pipette.id == "test_1_id"
    assert ot2.hardware_specific_attributes.right_pipette.model == "test_2"
    assert ot2.hardware_specific_attributes.right_pipette.id == "test_2_id"
