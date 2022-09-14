"""Tests to confirm that ConcreteCANServerServiceBuilder builds the CAN Server Service correctly."""

from typing import Any, Dict

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.conversion import (
    ConcreteCANServerServiceBuilder,
)
from emulation_system.consts import DEV_DOCKERFILE_NAME, DOCKERFILE_NAME
from tests.compose_file_creator.conversion_logic.conftest import (
    FAKE_COMMIT_ID,
    build_args_are_none,
    get_source_code_build_args,
    partial_string_in_mount,
)


@pytest.fixture
def remote_can_latest(ot3_only: Dict[str, Any]) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    can-server-source-type is set to remote.
    can-server-source-location is set to latest.
    """
    return parse_obj_as(SystemConfigurationModel, ot3_only)


@pytest.fixture
def remote_can_commit_id(ot3_only: Dict[str, Any]) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    can-server-source-type is set to remote.
    can-server-source-location is set a commit id.
    """
    ot3_only["robot"]["can-server-source-location"] = FAKE_COMMIT_ID
    return parse_obj_as(SystemConfigurationModel, ot3_only)


@pytest.fixture
def local_can(ot3_only: Dict[str, Any], opentrons_dir: str) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    can-server-source-type is set to local.
    can-server-source-location is set to a monorepo dir.
    """
    ot3_only["robot"]["can-server-source-type"] = "local"
    ot3_only["robot"]["can-server-source-location"] = opentrons_dir

    return parse_obj_as(SystemConfigurationModel, ot3_only)


@pytest.mark.parametrize(
    "config_model, dev",
    [
        (lazy_fixture("remote_can_latest"), True),
        (lazy_fixture("remote_can_latest"), False),
        (lazy_fixture("local_can"), True),
        (lazy_fixture("local_can"), False),
    ],
)
def test_simple_can_server_values(
    config_model: SystemConfigurationModel,
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for values that are the same for all configurations of a CANServer."""
    service = ConcreteCANServerServiceBuilder(
        config_model, testing_global_em_config, dev=dev
    ).build_service()

    expected_dockerfile_name = DEV_DOCKERFILE_NAME if dev else DOCKERFILE_NAME

    assert service.container_name == "can-server"
    assert isinstance(service.build, BuildItem)
    assert isinstance(service.build.context, str)
    assert "opentrons-emulation/docker/" in service.build.context
    assert service.build.dockerfile == expected_dockerfile_name
    assert isinstance(service.networks, list)
    assert len(service.networks) == 2
    assert "can-network" in service.networks
    assert "local-network" in service.networks

    assert service.tty

    assert service.command is None
    assert service.depends_on is None
    assert service.environment is None


@pytest.mark.parametrize(
    "config, expected_url",
    [
        (lazy_fixture("remote_can_latest"), lazy_fixture("opentrons_head")),
        (lazy_fixture("remote_can_commit_id"), lazy_fixture("opentrons_commit")),
    ],
)
def test_can_server_remote(
    config: SystemConfigurationModel,
    testing_global_em_config: OpentronsEmulationConfiguration,
    expected_url: str,
) -> None:
    """Tests for values that are the same for all remote configurations of a CANServer."""
    service = ConcreteCANServerServiceBuilder(
        config, testing_global_em_config, dev=True
    ).build_service()
    assert service.image == "can-server-remote"
    assert isinstance(service.build, BuildItem)
    assert isinstance(service.build.context, str)
    assert service.build.target == "can-server-remote"
    assert service.volumes is None
    assert get_source_code_build_args(service) == {
        RepoToBuildArgMapping.OPENTRONS.value: expected_url
    }


def test_can_server_local(
    local_can: SystemConfigurationModel,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test for values for local configuration of a CANServer."""
    service = ConcreteCANServerServiceBuilder(
        local_can, testing_global_em_config, dev=True
    ).build_service()
    assert service.image == "can-server-local"
    assert isinstance(service.build, BuildItem)
    assert isinstance(service.build.context, str)
    assert service.build.target == "can-server-local"
    assert build_args_are_none(service)

    volumes = service.volumes
    assert volumes is not None
    assert partial_string_in_mount("opentrons:/opentrons", volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", volumes)
    assert partial_string_in_mount("opentrons-python-dist:/dist", volumes)
