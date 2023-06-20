"""Tests to confirm that local-ot3-firmware-builder container is created correctly."""

from typing import Any, Dict, cast

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.compose_file_creator.conversion.service_builders import (
    OT3FirmwareBuilderService,
)
from tests.validation_helper_functions import (
    build_args_are_none,
    get_source_code_build_args,
)


@pytest.mark.parametrize(
    "config_model",
    [
        lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"),
        lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"),
        lazy_fixture("ot3_local_everything"),
    ],
)
def test_simple_values(
    config_model: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test values common to all 3 configs."""
    model = parse_obj_as(SystemConfigurationModel, config_model)
    service = OT3FirmwareBuilderService(
        model, testing_global_em_config, False
    ).build_service()

    assert service.image is not None
    assert service.image == "ot3-firmware-builder"
    assert service.container_name is not None
    assert service.container_name == "ot3-firmware-builder"
    assert service.tty
    assert isinstance(service.networks, list)
    assert len(service.networks) == 2
    assert "local-network" in service.networks
    assert "can-network" in service.networks
    assert service.command is None
    assert service.ports is None

    assert service.environment is not None
    env_root = cast(Dict[str, Any], service.environment.__root__)
    assert env_root is not None
    assert len(env_root.values()) == 2
    assert "LEFT_OT3_PIPETTE_DEFINITION" in env_root
    assert "RIGHT_OT3_PIPETTE_DEFINITION" in env_root


def test_local_ot3_firmware_remote_monorepo(
    ot3_local_ot3_firmware_remote_monorepo: Dict[str, Any],
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for when you are using local ot3-firmware and remote monorepo."""
    model = parse_obj_as(
        SystemConfigurationModel, ot3_local_ot3_firmware_remote_monorepo
    )
    service = OT3FirmwareBuilderService(
        model, testing_global_em_config, False
    ).build_service()

    monorepo_build_arg = OpentronsRepository.OPENTRONS.build_arg_name
    build_args = get_source_code_build_args(service)
    assert build_args is not None
    assert len(build_args) == 1
    assert monorepo_build_arg in build_args
    assert build_args[monorepo_build_arg] == opentrons_head

    volumes = service.volumes
    assert volumes is not None

    # TODO: Add volume checks when refactoring of local source is finished


def test_remote_ot3_firmware_local_monorepo(
    ot3_remote_ot3_firmware_local_monorepo: Dict[str, Any],
    ot3_firmware_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for when you are using remote ot3-firmware and local monorepo."""
    model = parse_obj_as(
        SystemConfigurationModel, ot3_remote_ot3_firmware_local_monorepo
    )
    service = OT3FirmwareBuilderService(
        model, testing_global_em_config, False
    ).build_service()

    ot3_firmware_build_arg = OpentronsRepository.OT3_FIRMWARE.build_arg_name
    build_args = get_source_code_build_args(service)
    assert build_args is not None
    assert len(build_args) == 1
    assert ot3_firmware_build_arg in build_args
    assert build_args[ot3_firmware_build_arg] == ot3_firmware_head

    volumes = service.volumes
    assert volumes is not None

    # TODO: Add volume checks when refactoring of local source is finished


def test_local_everything(
    ot3_local_everything: Dict[str, Any],
    opentrons_head: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for when you are using local ot3-firmware and local monorepo."""
    model = parse_obj_as(SystemConfigurationModel, ot3_local_everything)
    service = OT3FirmwareBuilderService(
        model, testing_global_em_config, False
    ).build_service()

    assert build_args_are_none(service)

    volumes = service.volumes
    assert volumes is not None

    # TODO: Add volume checks when refactoring of local source is finished
