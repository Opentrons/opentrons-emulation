"""Tests for OT-2 robot."""
from typing import (
    Any,
    Dict,
)

import pytest
from pydantic import (
    ValidationError,
    parse_obj_as,
)

from emulation_system.compose_file_creator.input.hardware_models import OT2InputModel
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    OpentronsRepository,
)
from tests.compose_file_creator.conftest import (
    OT2_EMULATION_LEVEL,
    OT2_ID,
    OT2_SOURCE_TYPE,
)


def test_default_ot2(ot2_default: Dict[str, Any]) -> None:
    """Confirm OT-2 is parsed correctly and default pipettes are applied."""
    ot2 = parse_obj_as(OT2InputModel, ot2_default)
    assert ot2.hardware == Hardware.OT2.value
    assert ot2.id == OT2_ID
    assert ot2.emulation_level == OT2_EMULATION_LEVEL
    assert ot2.source_type == OT2_SOURCE_TYPE
    assert ot2.hardware_specific_attributes.left_pipette.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.left_pipette.id == "P20SV202020070101"
    assert ot2.hardware_specific_attributes.right_pipette.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.right_pipette.id == "P20SV202020070101"


def test_ot2_with_custom_pipettes(ot2_with_pipettes: Dict[str, Any]) -> None:
    """Confirm OT-2 is parsed correctly and user-defined pipettes are applied."""
    ot2 = parse_obj_as(OT2InputModel, ot2_with_pipettes)
    assert ot2.hardware == Hardware.OT2.value
    assert ot2.id == OT2_ID
    assert ot2.emulation_level == OT2_EMULATION_LEVEL
    assert ot2.source_type == OT2_SOURCE_TYPE
    assert ot2.hardware_specific_attributes.left_pipette.model == "test_1"
    assert ot2.hardware_specific_attributes.left_pipette.id == "test_1_id"
    assert ot2.hardware_specific_attributes.right_pipette.model == "test_2"
    assert ot2.hardware_specific_attributes.right_pipette.id == "test_2_id"


def test_ot2_with_bad_emulation_level(ot2_bad_emulation_level: Dict[str, Any]) -> None:
    """Confirm that there is a validation error when a bad emulation level is passed."""
    with pytest.raises(ValidationError):
        parse_obj_as(OT2InputModel, ot2_bad_emulation_level)


def test_ot2_source_repos(ot2_default: Dict[str, Any]) -> None:
    """Confirm that defined source repos are correct."""
    temp = parse_obj_as(OT2InputModel, ot2_default)
    assert temp.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert temp.source_repos.hardware_repo_name is None
