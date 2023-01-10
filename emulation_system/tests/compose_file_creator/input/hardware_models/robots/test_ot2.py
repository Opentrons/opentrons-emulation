"""Tests for OT-2 robot."""
from typing import Any, Dict

import pytest
from pydantic import ValidationError, parse_obj_as

from emulation_system.compose_file_creator.config_file_settings import (
    Hardware,
    OpentronsRepository,
)
from emulation_system.compose_file_creator.input.hardware_models import OT2InputModel
from tests.compose_file_creator.conftest import EmulationLevels
from tests.conftest import OT2_ID


@pytest.fixture
def ot2_with_overridden_bound_port(ot2_model: Dict[str, Any]) -> Dict[str, Any]:
    """OT-2 with overridden bound-port."""
    ot2_model["bound-port"] = 2500
    return ot2_model


@pytest.fixture
def ot2_bad_emulation_level(ot2_model: Dict[str, Any]) -> Dict[str, Any]:
    """Return magnetic module configuration with an invalid emulation level."""
    ot2_model["emulation-level"] = EmulationLevels.HARDWARE.value
    return ot2_model


@pytest.fixture
def ot2_with_pipettes(ot2_model: Dict[str, Any]) -> Dict[str, Any]:
    """OT-2 using user-specified pipettes."""
    hardware_specific_attributes = ot2_model["hardware-specific-attributes"]
    hardware_specific_attributes["left-pipette"] = {}
    hardware_specific_attributes["left-pipette"]["model"] = "test_1"
    hardware_specific_attributes["left-pipette"]["id"] = "test_1_id"

    hardware_specific_attributes["right-pipette"] = {}
    hardware_specific_attributes["right-pipette"]["model"] = "test_2"
    hardware_specific_attributes["right-pipette"]["id"] = "test_2_id"
    return ot2_model


def test_default_ot2(ot2_model: Dict[str, Any]) -> None:
    """Confirm OT-2 is parsed correctly and default pipettes are applied."""
    ot2 = parse_obj_as(OT2InputModel, ot2_model)
    assert ot2.hardware == Hardware.OT2.value
    assert ot2.id == OT2_ID
    assert ot2.emulation_level == EmulationLevels.FIRMWARE.value
    assert ot2.exposed_port == 5000
    assert ot2.bound_port == 31950
    assert ot2.hardware_specific_attributes.left.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.left.id == "P20SV202020070101"
    assert ot2.hardware_specific_attributes.right.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.right.id == "P20SV202020070101"
    assert ot2.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert ot2.source_repos.hardware_repo_name is None


def test_ot2_with_overridden_bound_port(
    ot2_with_overridden_bound_port: Dict[str, Any]
) -> None:
    """Confirm bound-port is overridden correctly."""
    ot2 = parse_obj_as(OT2InputModel, ot2_with_overridden_bound_port)
    assert ot2.hardware == Hardware.OT2.value
    assert ot2.id == OT2_ID
    assert ot2.emulation_level == EmulationLevels.FIRMWARE.value
    assert ot2.exposed_port == 5000
    assert ot2.bound_port == 2500
    assert ot2.hardware_specific_attributes.left.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.left.id == "P20SV202020070101"
    assert ot2.hardware_specific_attributes.right.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.right.id == "P20SV202020070101"


def test_ot2_with_custom_pipettes(ot2_with_pipettes: Dict[str, Any]) -> None:
    """Confirm OT-2 is parsed correctly and user-defined pipettes are applied."""
    ot2 = parse_obj_as(OT2InputModel, ot2_with_pipettes)
    assert ot2.hardware == Hardware.OT2.value
    assert ot2.id == OT2_ID
    assert ot2.emulation_level == EmulationLevels.FIRMWARE.value
    assert ot2.exposed_port == 5000
    assert ot2.bound_port == 31950
    assert ot2.hardware_specific_attributes.left.model == "test_1"
    assert ot2.hardware_specific_attributes.left.id == "test_1_id"
    assert ot2.hardware_specific_attributes.right.model == "test_2"
    assert ot2.hardware_specific_attributes.right.id == "test_2_id"


def test_ot2_with_bad_emulation_level(ot2_bad_emulation_level: Dict[str, Any]) -> None:
    """Confirm that there is a validation error when a bad emulation level is passed."""
    with pytest.raises(ValidationError):
        parse_obj_as(OT2InputModel, ot2_bad_emulation_level)
