"""Tests for Magenetic Module."""
from typing import Any, Dict

import pytest
from pydantic import ValidationError, parse_obj_as

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    MagneticModuleInputModel,
)


@pytest.fixture
def magnetic_module_bad_emulation_level(
    magdeck_model: Dict[str, Any]
) -> Dict[str, Any]:
    """Return magnetic module configuration with an invalid emulation level."""
    magdeck_model["emulation-level"] = EmulationLevels.HARDWARE.value
    return magdeck_model


def test_default_magnetic_module(magdeck_model: Dict[str, Any]) -> None:
    """Confirm Magnetic Module is parsed correctly."""
    mag = parse_obj_as(MagneticModuleInputModel, magdeck_model)
    assert mag.hardware == Hardware.MAGNETIC_MODULE.value
    assert mag.emulation_level == EmulationLevels.FIRMWARE.value


def test_magnetic_module_with_bad_emulation_level(
    magnetic_module_bad_emulation_level: Dict[str, Any]
) -> None:
    """Confirm that there is a validation error when a bad emulation level is passed."""
    with pytest.raises(ValidationError):
        mag = parse_obj_as(
            MagneticModuleInputModel, magnetic_module_bad_emulation_level
        )


def test_magnetic_module_source_repos(magdeck_model: Dict[str, Any]) -> None:
    """Confirm that defined source repos are correct."""
    mag = parse_obj_as(MagneticModuleInputModel, magdeck_model)
    assert mag.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert mag.source_repos.hardware_repo_name is None
