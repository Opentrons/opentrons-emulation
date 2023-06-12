"""Testing pipette utils."""

import datetime
import json
from enum import Enum
from typing import Tuple

import pytest

from emulation_system.compose_file_creator.pipette_utils import get_robot_pipettes
from emulation_system.compose_file_creator.pipette_utils.lookups import (
    OT2PipetteLookup,
    OT3PipetteLookup,
    lookup_pipette,
)

VALID_OT2_PIPETTE_NAMES = [
    ("p20_single_gen2", OT2PipetteLookup.P20_SINGLE),
    ("P20 Single", OT2PipetteLookup.P20_SINGLE),
    ("p20_multi_gen2", OT2PipetteLookup.P20_MULTI),
    ("P20 Multi", OT2PipetteLookup.P20_MULTI),
    ("p300_single_gen2", OT2PipetteLookup.P300_SINGLE),
    ("P300 Single", OT2PipetteLookup.P300_SINGLE),
    ("p300_multi_gen2", OT2PipetteLookup.P300_MULTI),
    ("P300 Multi", OT2PipetteLookup.P300_MULTI),
    ("p1000_single_gen2", OT2PipetteLookup.P1000_SINGLE_GEN2),
    ("P1000 Single", OT2PipetteLookup.P1000_SINGLE_GEN2),
]

VALID_OT3_PIPETTE_NAMES = [
    ("p50_single", OT3PipetteLookup.P50_SINGLE),
    ("P50 Single", OT3PipetteLookup.P50_SINGLE),
    ("p50_multi", OT3PipetteLookup.P50_MULTI),
    ("P50 Multi", OT3PipetteLookup.P50_MULTI),
    ("p1000_single", OT3PipetteLookup.P1000_SINGLE),
    ("P1000 Single", OT3PipetteLookup.P1000_SINGLE),
    ("p1000_multi", OT3PipetteLookup.P1000_MULTI),
    ("P1000 Multi", OT3PipetteLookup.P1000_MULTI),
    ("p1000_96", OT3PipetteLookup.P1000_96),
    ("P1000 96 Channel", OT3PipetteLookup.P1000_96),
    ("p50_96", OT3PipetteLookup.P50_96),
    ("P50 96 Channel", OT3PipetteLookup.P50_96),
]

INVALID_PIPETTE_NAMES = [
    "p20_single_gen3",
    "p20_multi_gen3",
    "p10_single_gen1",
    "p10_multi_gen1",
    "P20 Multi GEN2",
]

EXPECTED_OT2_PIPETTE_NAME_ENUM = Enum(
    "OT2PipettesValidNames",
    [
        ("P20_SINGLE_GEN2_NAME", "p20_single_gen2"),
        ("P20_MULTI_GEN2_NAME", "p20_multi_gen2"),
        ("P300_SINGLE_GEN2_NAME", "p300_single_gen2"),
        ("P300_MULTI_GEN2_NAME", "p300_multi_gen2"),
        ("P1000_SINGLE_GEN2_NAME", "p1000_single_gen2"),
    ],
)

EXPECTED_OT3_PIPETTE_NAME_ENUM = Enum(
    "OT3PipettesValidNames",
    [
        ("P50_SINGLE_GEN3_NAME", "p50_single"),
        ("P50_MULTI_GEN3_NAME", "p50_multi"),
        ("P1000_SINGLE_GEN3_NAME", "p1000_single"),
        ("P1000_MULTI_GEN3_NAME", "p1000_multi"),
        ("P1000_96_NAME", "p1000_96"),
        ("P50_96_NAME", "p50_96"),
    ],
)


@pytest.mark.parametrize("pipette_name, expected_enum", VALID_OT2_PIPETTE_NAMES)
def test_valid_ot2_pipette_names(
    pipette_name: str, expected_enum: Tuple[str, OT2PipetteLookup]
) -> None:
    """Tests looking up OT2 pipette enum value by name."""
    actual_enum = lookup_pipette(pipette_name, "ot2")
    assert actual_enum == expected_enum


@pytest.mark.parametrize("pipette_name, expected_enum", VALID_OT3_PIPETTE_NAMES)
def test_valid_ot3_pipette_names(
    pipette_name: str, expected_enum: Tuple[str, OT3PipetteLookup]
) -> None:
    """Tests looking up OT3 pipette enum value by name."""
    actual_enum = lookup_pipette(pipette_name, "ot3")
    assert actual_enum == expected_enum


@pytest.mark.parametrize("pipette_name", INVALID_PIPETTE_NAMES)
def test_invalid_pipette_names(pipette_name: str) -> None:
    """Tests ensuring invalid pipette name throws error."""
    with pytest.raises(ValueError):
        lookup_pipette(pipette_name, "ot2")
    with pytest.raises(ValueError):
        lookup_pipette(pipette_name, "ot3")


def test_ot3_pipette_env_var() -> None:
    """Tests generating OT3 pipette env var."""
    pipettes = get_robot_pipettes("ot3", "P50 Single", "P1000 Multi")
    left_expected_env_var = {
        "LEFT_OT3_PIPETTE_DEFINITION": json.dumps(
            {
                "pipette_name": "p50_single",
                "pipette_model": 34,
                "pipette_serial_code": datetime.datetime.now().strftime("%m%d%Y"),
                "eeprom_file_name": "eeprom.bin",
            }
        )
    }

    right_expected_env_var = {
        "RIGHT_OT3_PIPETTE_DEFINITION": json.dumps(
            {
                "pipette_name": "p1000_multi",
                "pipette_model": 34,
                "pipette_serial_code": datetime.datetime.now().strftime("%m%d%Y"),
                "eeprom_file_name": "eeprom.bin",
            }
        )
    }

    assert pipettes.get_left_pipette_env_var() == left_expected_env_var
    assert pipettes.get_right_pipette_env_var() == right_expected_env_var


def test_pipette_name_enum() -> None:
    """Tests getting pipette name enum."""
    ot2_actual_members = {value.value for value in OT2PipetteLookup.get_valid_pipette_names().__members__.values()}  # type: ignore[attr-defined]
    ot3_actual_members = {value.value for value in OT3PipetteLookup.get_valid_pipette_names().__members__.values()}  # type: ignore[attr-defined]

    ot2_expected_members = {item[0] for item in VALID_OT2_PIPETTE_NAMES}
    ot3_expected_members = {item[0] for item in VALID_OT3_PIPETTE_NAMES}

    assert ot2_actual_members == ot2_expected_members
    assert ot3_actual_members == ot3_expected_members


def test_pipette_restrictions() -> None:
    """Test pipette restrictions."""
    # Left Mount Only Exception
    with pytest.raises(ValueError) as err:
        get_robot_pipettes("ot3", None, "P1000 96 Channel")
    assert "is restricted to left mount only." in str(err.value)

    # Blocks Other Mount Exception
    with pytest.raises(ValueError) as err:
        get_robot_pipettes("ot3", "P1000 96 Channel", "P50 Single")
    assert '"P1000 96 Channel" blocks both pipette mounts'
