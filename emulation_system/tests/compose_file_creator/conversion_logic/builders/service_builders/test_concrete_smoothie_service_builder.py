"""Tests to confirm that ConcreteCANServerServiceBuilder builds the CAN Server Service correctly."""
import json
from typing import (
    Any,
    Dict,
    cast,
)

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import (
    OpentronsEmulationConfiguration,
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.config_file_settings import (
    PipetteSettings,
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.conversion import (
    ConcreteSmoothieServiceBuilder,
)
from emulation_system.compose_file_creator.output.compose_file_model import ListOrDict
from emulation_system.consts import (
    DEV_DOCKERFILE_NAME,
    DOCKERFILE_NAME,
)
from tests.compose_file_creator.conversion_logic.conftest import (
    FAKE_COMMIT_ID,
    build_args_are_none,
    get_source_code_build_args,
    partial_string_in_mount,
)


@pytest.fixture
def remote_source_latest(ot2_only: Dict[str, Any]) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    source-type is set to remote.
    source-location is set to latest.
    """
    ot2_only["robot"]["source-type"] = "remote"
    ot2_only["robot"]["source-location"] = "latest"
    return parse_obj_as(SystemConfigurationModel, ot2_only)


@pytest.fixture
def remote_source_commit_id(ot2_only: Dict[str, Any]) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    source-type is set to remote.
    source-location is set a commit id.
    """
    ot2_only["robot"]["source-type"] = "remote"
    ot2_only["robot"]["source-location"] = FAKE_COMMIT_ID
    return parse_obj_as(SystemConfigurationModel, ot2_only)


@pytest.fixture
def local_source(
    ot2_only: Dict[str, Any], opentrons_dir: str
) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    source-type is set to local.
    source-location is set to a monorepo dir.
    """
    ot2_only["robot"]["source-type"] = "local"
    ot2_only["robot"]["source-location"] = opentrons_dir

    return parse_obj_as(SystemConfigurationModel, ot2_only)


@pytest.mark.parametrize(
    "config_model, dev",
    [
        (lazy_fixture("remote_source_latest"), True),
        (lazy_fixture("remote_source_latest"), False),
        (lazy_fixture("remote_source_commit_id"), True),
        (lazy_fixture("remote_source_commit_id"), False),
        (lazy_fixture("local_source"), True),
        (lazy_fixture("local_source"), False),
    ],
)
def test_simple_smoothie_values(
    config_model: SystemConfigurationModel,
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for values that are the same for all configurations of a Smoothie Service."""
    service = ConcreteSmoothieServiceBuilder(
        config_model, testing_global_em_config, dev=dev
    ).build_service()

    expected_dockerfile_name = DEV_DOCKERFILE_NAME if dev else DOCKERFILE_NAME
    default_pipette_definition = {
        "model": PipetteSettings().model,
        "id": PipetteSettings().id,
    }

    assert service.container_name == "smoothie"
    assert isinstance(service.build, BuildItem)
    assert isinstance(service.build.context, str)
    assert "opentrons-emulation/docker/" in service.build.context
    assert service.build.dockerfile == expected_dockerfile_name
    assert isinstance(service.networks, list)
    assert len(service.networks) == 1
    assert "local-network" in service.networks

    smoothie_environment = service.environment
    assert smoothie_environment is not None
    assert isinstance(smoothie_environment, ListOrDict)
    env_root = cast(Dict[str, Any], smoothie_environment.__root__)
    assert env_root is not None
    assert len(env_root.values()) == 1
    assert "OT_EMULATOR_smoothie" in env_root
    smoothie_env_dict = json.loads(env_root["OT_EMULATOR_smoothie"])
    assert smoothie_env_dict is not None
    assert "left" in smoothie_env_dict
    assert "right" in smoothie_env_dict
    assert "port" in smoothie_env_dict
    assert smoothie_env_dict["left"] == default_pipette_definition
    assert smoothie_env_dict["right"] == default_pipette_definition
    assert smoothie_env_dict["port"] == 11000

    assert service.tty

    assert service.command is None
    assert service.depends_on is None


@pytest.mark.parametrize(
    "config, expected_url",
    [
        (lazy_fixture("remote_source_latest"), lazy_fixture("opentrons_head")),
        (lazy_fixture("remote_source_commit_id"), lazy_fixture("opentrons_commit")),
    ],
)
def test_smoothie_remote(
    config: SystemConfigurationModel,
    testing_global_em_config: OpentronsEmulationConfiguration,
    expected_url: str,
) -> None:
    """Tests for values that are the same for all remote configurations of a Smoothie Service."""
    service = ConcreteSmoothieServiceBuilder(
        config, testing_global_em_config, dev=True
    ).build_service()
    assert service.image == "smoothie-remote:latest"
    assert isinstance(service.build, BuildItem)
    assert isinstance(service.build.context, str)
    assert service.build.target == "smoothie-remote"
    assert service.volumes is None
    assert get_source_code_build_args(service) == {
        RepoToBuildArgMapping.OPENTRONS.value: expected_url
    }


def test_smoothie_local(
    local_source: SystemConfigurationModel,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test for values for local configuration of a Smoothie Service."""
    service = ConcreteSmoothieServiceBuilder(
        local_source, testing_global_em_config, dev=True
    ).build_service()
    assert service.image == "smoothie-local:latest"
    assert isinstance(service.build, BuildItem)
    assert isinstance(service.build.context, str)
    assert service.build.target == "smoothie-local"
    assert build_args_are_none(service)

    volumes = service.volumes
    assert volumes is not None
    assert partial_string_in_mount("opentrons:/opentrons", volumes)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", volumes)
    assert partial_string_in_mount("opentrons-python-dist:/dist", volumes)
