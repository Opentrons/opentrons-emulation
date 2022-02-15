"""Tests for Magenetic Module."""
from typing import Any, Dict

import pytest
from pydantic import ValidationError, parse_obj_as

from emulation_system.compose_file_creator.input.hardware_models import (
    MagneticModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    OpentronsRepository,
)
from tests.compose_file_creator.conftest import (
    MAGNETIC_MODULE_EMULATION_LEVEL,
    MAGNETIC_MODULE_ID,
    MAGNETIC_MODULE_SOURCE_TYPE,
)


def test_default_magnetic_module(magnetic_module_default: Dict[str, Any]) -> None:
    """Confirm Magnetic Module is parsed correctly."""
    mag = parse_obj_as(MagneticModuleInputModel, magnetic_module_default)
    assert mag.hardware == Hardware.MAGNETIC_MODULE.value
    assert mag.id == MAGNETIC_MODULE_ID
    assert mag.emulation_level == MAGNETIC_MODULE_EMULATION_LEVEL
    assert mag.source_type == MAGNETIC_MODULE_SOURCE_TYPE


def test_magnetic_module_with_bad_emulation_level(
    magnetic_module_bad_emulation_level: Dict[str, Any]
) -> None:
    """Confirm that there is a validation error when a bad emulation level is passed."""
    with pytest.raises(ValidationError):
        parse_obj_as(MagneticModuleInputModel, magnetic_module_bad_emulation_level)


def test_magnetic_module_source_repos(magnetic_module_default: Dict[str, Any]) -> None:
    """Confirm that defined source repos are correct."""
    mage = parse_obj_as(MagneticModuleInputModel, magnetic_module_default)
    assert mage.source_repos.firmware_repo_name == OpentronsRepository.OPENTRONS
    assert mage.source_repos.hardware_repo_name is None
