"""Tests to confirm that ConcreteSmoothieServiceBuilder builds the CAN Server Service correctly."""
import json
from typing import Any, Callable, Dict, cast

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.config_file_settings import (
    PipetteSettings,
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.conversion import (
    ConcreteSmoothieServiceBuilder,
)
from emulation_system.compose_file_creator.output.compose_file_model import ListOrDict
from emulation_system.consts import DEV_DOCKERFILE_NAME, DOCKERFILE_NAME
from tests.compose_file_creator.conversion_logic.conftest import (
    build_args_are_none,
    get_source_code_build_args,
    partial_string_in_mount,
)


@pytest.fixture
def local_source(make_config: Callable) -> Dict[str, Any]:
    """Gets SystemConfigurationModel.

    source-type is set to local.
    source-location is set to a monorepo dir.
    """
    return make_config(robot="ot2", monorepo_source="path")


@pytest.fixture
def remote_source_commit_id(make_config: Callable) -> Dict[str, Any]:
    """Gets SystemConfigurationModel.

    source-type is set to local.
    source-location is set to a monorepo dir.
    """
    return make_config(robot="ot2", monorepo_source="commit_id")


@pytest.mark.parametrize(
    "model_dict, dev",
    [
        (lazy_fixture("ot2_only"), True),
        (lazy_fixture("ot2_only"), False),
        (lazy_fixture("remote_source_commit_id"), True),
        (lazy_fixture("remote_source_commit_id"), False),
        (lazy_fixture("local_source"), True),
        (lazy_fixture("local_source"), False),
    ],
)
def test_simple_smoothie_values(
    model_dict: Dict[str, Any],
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for values that are the same for all configurations of a Smoothie Service."""
    config_model = parse_obj_as(SystemConfigurationModel, model_dict)
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
    assert service.build.target == "smoothie-local"
    assert build_args_are_none(service)

    assert partial_string_in_mount("opentrons:/opentrons", service)
    assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", service)
    assert partial_string_in_mount("opentrons-python-dist:/dist", service)
