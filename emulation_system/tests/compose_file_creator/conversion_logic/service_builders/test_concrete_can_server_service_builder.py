"""Tests to confirm that CANServerService builds the CAN Server Service correctly."""

from typing import Any, Callable, Dict

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.conversion import CANServerService
from emulation_system.consts import DEV_DOCKERFILE_NAME, DOCKERFILE_NAME
from tests.validation_helper_functions import (
    build_args_are_none,
    partial_string_in_mount,
)


@pytest.fixture
def remote_can_commit_id(make_config: Callable) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    can-server-source-type is set to remote.
    can-server-source-location is set a commit id.
    """
    return make_config(robot="ot3", monorepo_source="commit_id")


@pytest.fixture
def local_can(make_config: Callable) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    can-server-source-type is set to local.
    can-server-source-location is set to a monorepo dir.
    """
    return make_config(robot="ot3", monorepo_source="path")


@pytest.mark.parametrize(
    "model_dict, dev",
    [
        (lazy_fixture("ot3_only"), True),
        (lazy_fixture("ot3_only"), False),
        (lazy_fixture("remote_can_commit_id"), True),
        (lazy_fixture("remote_can_commit_id"), False),
        (lazy_fixture("local_can"), True),
        (lazy_fixture("local_can"), False),
    ],
)
def test_simple_can_server_values(
    model_dict: Dict[str, Any],
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for values that are the same for all configurations of a CANServer."""
    config_model = parse_obj_as(SystemConfigurationModel, model_dict)
    service = CANServerService(
        config_model, testing_global_em_config, dev=dev
    ).build_service()

    expected_dockerfile_name = DEV_DOCKERFILE_NAME if dev else DOCKERFILE_NAME

    assert service.container_name == "can-server"
    assert service.image == "can-server"

    assert isinstance(service.build, BuildItem)
    assert isinstance(service.build.context, str)
    assert "opentrons-emulation/docker/" in service.build.context
    assert service.build.dockerfile == expected_dockerfile_name
    assert service.build.target == "can-server"
    assert build_args_are_none(service)

    assert isinstance(service.networks, list)
    assert len(service.networks) == 2
    assert "can-network" in service.networks
    assert "local-network" in service.networks

    assert service.tty

    assert service.command is None
    assert service.depends_on is None
    assert service.environment is None

    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", service)
    assert partial_string_in_mount("monorepo-wheels:/dist", service)
