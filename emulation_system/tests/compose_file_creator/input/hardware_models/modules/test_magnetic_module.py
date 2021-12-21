"""Tests for Magenetic Module."""
from typing import Dict, Any

import py
import pytest
from pydantic import (
    ValidationError,
    parse_obj_as,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    MagneticModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    EmulationLevels,
    OpentronsRepository,
    SourceType,
)

ID = "my-magnetic"
HARDWARE = Hardware.MAGNETIC_MODULE.value
EMULATION_LEVEL = EmulationLevels.FIRMWARE.value
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


@pytest.fixture
def bad_emulation_level(magnetic_module_default: Dict[str, Any]) -> Dict[str, Any]:
    """Return magnetic module configuration with an invalid emulation level."""
    magnetic_module_default["emulation-level"] = EmulationLevels.HARDWARE.value
    return magnetic_module_default


def test_default_magnetic_module(magnetic_module_default: Dict[str, Any]) -> None:
    """Confirm Magnetic Module is parsed correctly."""
    mag = parse_obj_as(MagneticModuleInputModel, magnetic_module_default)
    assert mag.hardware == HARDWARE
    assert mag.id == ID
    assert mag.emulation_level == EMULATION_LEVEL
    assert mag.source_type == SOURCE_TYPE


def test_magnetic_module_with_bad_emulation_level(
    bad_emulation_level: Dict[str, Any]
) -> None:
    """Confirm that there is a validation error when a bad emulation level is passed."""
    with pytest.raises(ValidationError):
        parse_obj_as(MagneticModuleInputModel, bad_emulation_level)


def test_magnetic_module_source_repos(magnetic_module_default: Dict[str, Any]) -> None:
    """Confirm that defined source repos are correct."""
    mage = parse_obj_as(MagneticModuleInputModel, magnetic_module_default)
    assert mage.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert mage.source_repos.hardware_repo_name is None
