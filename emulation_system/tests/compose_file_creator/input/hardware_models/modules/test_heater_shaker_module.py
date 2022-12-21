"""Tests for heater-shaker module."""
from typing import Any, Dict

import pytest
from pydantic import parse_obj_as

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    HeaterShakerModes,
    OpentronsRepository,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
)


@pytest.fixture
def heater_shaker_use_stdin(heater_shaker_model) -> Dict[str, Any]:
    """Heater-shaker dictionary with mode set to stdin."""
    heater_shaker_model["hardware-specific-attributes"] = {
        "mode": HeaterShakerModes.STDIN
    }
    return heater_shaker_model


def test_default_heater_shaker(heater_shaker_model: Dict[str, Any]) -> None:
    """Confirm Heater-Shaker is parsed right and default mode of socket is set."""
    hs = parse_obj_as(HeaterShakerModuleInputModel, heater_shaker_model)
    assert hs.hardware == Hardware.HEATER_SHAKER_MODULE.value
    assert hs.emulation_level == EmulationLevels.HARDWARE.value
    assert hs.hardware_specific_attributes.mode == HeaterShakerModes.SOCKET


def test_heater_shaker_with_stdin(heater_shaker_use_stdin: Dict[str, Any]) -> None:
    """Confirm Heater-Shaker is parsed right and stdin mode is picked up."""
    hs = parse_obj_as(HeaterShakerModuleInputModel, heater_shaker_use_stdin)
    assert hs.hardware == Hardware.HEATER_SHAKER_MODULE.value
    assert hs.emulation_level == EmulationLevels.HARDWARE.value
    assert hs.hardware_specific_attributes.mode == HeaterShakerModes.STDIN


def test_heater_shaker_source_repos(heater_shaker_model: Dict[str, Any]) -> None:
    """Confirm that defined source repos are correct."""
    hs = parse_obj_as(HeaterShakerModuleInputModel, heater_shaker_model)
    assert hs.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert hs.source_repos.hardware_repo_name == OpentronsRepository.OPENTRONS_MODULES
