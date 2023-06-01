"""Testing pipette utils."""

import datetime
import json
from enum import Enum
from typing import Tuple

import pytest

from emulation_system.compose_file_creator.pipette_utils import (
    OT2Pipettes,
    OT3Pipettes,
)

VALID_OT2_PIPETTE_NAMES = [
    ("p20_single_gen2", OT2Pipettes.P20_SINGLE),
    ("P20 Single", OT2Pipettes.P20_SINGLE),
    ("p20_multi_gen2", OT2Pipettes.P20_MULTI),
    ("P20 Multi", OT2Pipettes.P20_MULTI),
    ("p300_single_gen2", OT2Pipettes.P300_SINGLE),
    ("P300 Single", OT2Pipettes.P300_SINGLE),
    ("p300_multi_gen2", OT2Pipettes.P300_MULTI),
    ("P300 Multi", OT2Pipettes.P300_MULTI),
    ("p1000_single_gen2", OT2Pipettes.P1000_SINGLE_GEN2),
    ("P1000 Single", OT2Pipettes.P1000_SINGLE_GEN2),
]

VALID_OT3_PIPETTE_NAMES = [
    ("p50_single_gen3", OT3Pipettes.P50_SINGLE),
    ("P50 Single", OT3Pipettes.P50_SINGLE),
    ("p50_multi_gen3", OT3Pipettes.P50_MULTI),
    ("P50 Multi", OT3Pipettes.P50_MULTI),
    ("p1000_single_gen3", OT3Pipettes.P1000_SINGLE),
    ("P1000 Single", OT3Pipettes.P1000_SINGLE),
    ("p1000_multi_gen3", OT3Pipettes.P1000_MULTI),
    ("P1000 Multi", OT3Pipettes.P1000_MULTI),
    ("p1000_96", OT3Pipettes.P1000_96),
    ("P1000 96 Channel", OT3Pipettes.P1000_96),
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
        ("P50_SINGLE_GEN3_NAME", "p50_single_gen3"),
        ("P50_MULTI_GEN3_NAME", "p50_multi_gen3"),
        ("P1000_SINGLE_GEN3_NAME", "p1000_single_gen3"),
        ("P1000_MULTI_GEN3_NAME", "p1000_multi_gen3"),
        ("P1000_96_NAME", "p1000_96"),
    ],
)


@pytest.mark.parametrize("pipette_name, expected_enum", VALID_OT2_PIPETTE_NAMES)
def test_valid_ot2_pipette_names(
    pipette_name: str, expected_enum: Tuple[str, OT2Pipettes]
) -> None:
    """Tests looking up OT2 pipette enum value by name."""
    actual_enum = OT2Pipettes.lookup_by_name(pipette_name)
    assert actual_enum == expected_enum


@pytest.mark.parametrize("pipette_name, expected_enum", VALID_OT3_PIPETTE_NAMES)
def test_valid_ot3_pipette_names(
    pipette_name: str, expected_enum: Tuple[str, OT3Pipettes]
) -> None:
    """Tests looking up OT3 pipette enum value by name."""
    actual_enum = OT3Pipettes.lookup_by_name(pipette_name)
    assert actual_enum == expected_enum


@pytest.mark.parametrize("pipette_name", INVALID_PIPETTE_NAMES)
def test_invalid_pipette_names(pipette_name: str) -> None:
    """Tests ensuring invalid pipette name throws error."""
    with pytest.raises(ValueError):
        OT2Pipettes.lookup_by_name(pipette_name)
    with pytest.raises(ValueError):
        OT3Pipettes.lookup_by_name(pipette_name)


@pytest.mark.parametrize(
    "model, serial_code, expected_model, expected_serial_code",
    [
        (2, None, "02", datetime.datetime.now().strftime("%m%d%Y")),
        (3, "abc123", "03", "abc123"),
    ],
)
def test_ot3_pipette_env_var(
    model: int, serial_code: str | None, expected_model: str, expected_serial_code: str
) -> None:
    """Tests generating OT3 pipette env var."""
    pipette_info = OT3Pipettes.P50_SINGLE
    expected_env_var = {
        "OT3_PIPETTE_DEFINITION": json.dumps(
            {
                "pipette_name": "p50_single_gen3",
                "pipette_model": expected_model,
                "pipette_serial_code": expected_serial_code,
            }
        )
    }

    assert (
        pipette_info.generate_pipette_env_var_def(model, serial_code).to_env_var()
        == expected_env_var
    )


def test_ot3_pipette_env_var_raises_error_on_model() -> None:
    """Tests generating OT3 pipette env var raises error if model is less than 0 or greater than 99."""
    with pytest.raises(ValueError) as err:
        OT3Pipettes.P50_SINGLE.generate_pipette_env_var_def(-1, None)
        assert "Model must be between" in str(err)

    with pytest.raises(ValueError) as err:
        OT3Pipettes.P50_SINGLE.generate_pipette_env_var_def(100, None)
        assert "Model must be between" in str(err)


def test_ot3_pipette_env_var_raises_error_on_serial_code_not_alphanumeric() -> None:
    """Tests generating OT3 pipette env var raises error if serial code is alphanumeric."""
    with pytest.raises(ValueError) as err:
        OT3Pipettes.P50_SINGLE.generate_pipette_env_var_def(3, "abc-?>")
        assert "Serial code must be alphanumeric." == str(err)


def test_ot3_pipette_env_var_raises_error_on_serial_code_too_short() -> None:
    """Tests generating OT3 pipette env var raises error if serial code is too short."""
    with pytest.raises(ValueError) as err:
        OT3Pipettes.P50_SINGLE.generate_pipette_env_var_def(3, "")
        assert "Serial code is too short. Min length is 1 character." == str(err)


def test_ot3_pipette_env_var_raises_error_on_serial_code_too_long() -> None:
    """Tests generating OT3 pipette env var raises error if serial code is too long."""
    with pytest.raises(ValueError) as err:
        OT3Pipettes.P50_SINGLE.generate_pipette_env_var_def(3, "a" * 13)
        assert "Serial code is too long. Max length is 12 characters." == str(err)


def test_pipette_name_enum() -> None:
    """Tests getting pipette name enum."""
    ot2_actual_members = {value.value for value in OT2Pipettes.valid_pipette_name_enum().__members__.values()}  # type: ignore[attr-defined]
    ot3_actual_members = {value.value for value in OT3Pipettes.valid_pipette_name_enum().__members__.values()}  # type: ignore[attr-defined]

    ot2_expected_members = {item[0] for item in VALID_OT2_PIPETTE_NAMES}
    ot3_expected_members = {item[0] for item in VALID_OT3_PIPETTE_NAMES}

    assert ot2_actual_members == ot2_expected_members
    assert ot3_actual_members == ot3_expected_members
