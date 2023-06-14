"""Tests to confirm that builder creation logic is correct."""

from typing import Any, Dict

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_only"),
        lazy_fixture("ot3_remote_everything_branch"),
        lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"),
        lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"),
        lazy_fixture("ot3_local_everything"),
    ],
)
def test_local_ot3_builder_required(config: Dict[str, Any]) -> None:
    """Test all configurations that require local-ot3-firmware-builder."""
    config_model = parse_obj_as(SystemConfigurationModel, config)
    assert config_model.local_ot3_builder_required


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot2_only"),
        lazy_fixture("ot2_remote_everything_branch"),
        lazy_fixture("ot2_local_source"),
        lazy_fixture("heater_shaker_module_hardware_local"),
        lazy_fixture("heater_shaker_module_hardware_remote"),
        lazy_fixture("thermocycler_module_firmware_local"),
        lazy_fixture("thermocycler_module_hardware_local"),
        lazy_fixture("thermocycler_module_firmware_remote"),
        lazy_fixture("thermocycler_module_hardware_remote"),
        lazy_fixture("temperature_module_firmware_local"),
        lazy_fixture("temperature_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_local"),
    ],
)
def test_local_ot3_builder_not_required(config: Dict[str, Any]) -> None:
    """Test all configurations that do not require local-ot3-firmware-builder."""
    config_model = parse_obj_as(SystemConfigurationModel, config)
    assert not config_model.local_ot3_builder_required


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("heater_shaker_module_hardware_local"),
        lazy_fixture("thermocycler_module_hardware_local"),
        lazy_fixture("heater_shaker_module_hardware_remote"),
        lazy_fixture("thermocycler_module_hardware_remote"),
    ],
)
def test_local_opentrons_modules_builder_required(config: Dict[str, Any]) -> None:
    """Test all configurations that require local-opentrons-modules-builder."""
    config_model = parse_obj_as(SystemConfigurationModel, config)
    assert config_model.local_opentrons_modules_builder_required


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot2_only"),
        lazy_fixture("ot3_only"),
        lazy_fixture("ot3_remote_everything_branch"),
        lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"),
        lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"),
        lazy_fixture("ot3_local_everything"),
        lazy_fixture("ot2_remote_everything_branch"),
        lazy_fixture("ot2_local_source"),
        lazy_fixture("thermocycler_module_firmware_local"),
        lazy_fixture("thermocycler_module_firmware_remote"),
        lazy_fixture("temperature_module_firmware_local"),
        lazy_fixture("temperature_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_local"),
    ],
)
def test_local_opentrons_modules_builder_not_required(config: Dict[str, Any]) -> None:
    """Test all configurations that do not require local-opentrons-modules-builder."""
    config_model = parse_obj_as(SystemConfigurationModel, config)
    assert not config_model.local_opentrons_modules_builder_required


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot2_only"),
        lazy_fixture("ot3_only"),
        lazy_fixture("ot3_remote_everything_branch"),
        lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"),
        lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"),
        lazy_fixture("ot3_local_everything"),
        lazy_fixture("ot2_remote_everything_branch"),
        lazy_fixture("ot2_local_source"),
        lazy_fixture("thermocycler_module_firmware_local"),
        lazy_fixture("temperature_module_firmware_local"),
        lazy_fixture("magnetic_module_firmware_local"),
        lazy_fixture("magnetic_module_firmware_remote"),
        lazy_fixture("thermocycler_module_firmware_remote"),
        lazy_fixture("temperature_module_firmware_remote"),
    ],
)
def test_local_monorepo_builder_required(config: Dict[str, Any]) -> None:
    """Test all configurations that require local-monorepo-builder."""
    config_model = parse_obj_as(SystemConfigurationModel, config)
    assert config_model.local_monorepo_builder_required


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("heater_shaker_module_hardware_local"),
        lazy_fixture("heater_shaker_module_hardware_remote"),
        lazy_fixture("thermocycler_module_hardware_local"),
        lazy_fixture("thermocycler_module_hardware_remote"),
    ],
)
def test_local_monorepo_builder_not_required(config: Dict[str, Any]) -> None:
    """Test all configurations that do not require local-monorepo-builder."""
    config_model = parse_obj_as(SystemConfigurationModel, config)
    assert not config_model.local_monorepo_builder_required
