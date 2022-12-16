"""Tests to confirm that ConcreteCANServerServiceBuilder builds the CAN Server Service correctly."""
from typing import Any, Dict, cast

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.conversion import (
    ConcreteEmulatorProxyServiceBuilder,
)
from emulation_system.compose_file_creator.output.compose_file_model import ListOrDict
from emulation_system.consts import DEV_DOCKERFILE_NAME, DOCKERFILE_NAME
from tests.compose_file_creator.conversion_logic.conftest import (
    get_source_code_build_args,
)


@pytest.fixture
def ot2_system_config(ot2_only: Dict[str, Any]) -> SystemConfigurationModel:
    """Creates SystemConfigurationModel with just an OT-2."""
    return parse_obj_as(SystemConfigurationModel, ot2_only)


@pytest.fixture
def ot3_system_config(ot3_only: Dict[str, Any]) -> SystemConfigurationModel:
    """Creates SystemConfigurationModel with just an OT-3."""
    return parse_obj_as(SystemConfigurationModel, ot3_only)


@pytest.mark.parametrize(
    "config_model, dev",
    [
        (lazy_fixture("ot2_system_config"), True),
        (lazy_fixture("ot2_system_config"), False),
        (lazy_fixture("ot3_system_config"), True),
        (lazy_fixture("ot3_system_config"), False),
    ],
)
def test_simple_emulator_proxy_values(
    config_model: SystemConfigurationModel,
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
    opentrons_head: str,
) -> None:
    """Tests for values that are the same for all configurations of an Emulator Proxy."""
    service = ConcreteEmulatorProxyServiceBuilder(
        config_model, testing_global_em_config, dev=dev
    ).build_service()

    expected_dockerfile_name = DEV_DOCKERFILE_NAME if dev else DOCKERFILE_NAME

    assert service.container_name == "emulator-proxy"
    assert service.image == "emulator-proxy-remote:latest"
    assert isinstance(service.build, BuildItem)
    assert isinstance(service.build.context, str)
    assert service.build.target == "emulator-proxy-remote"
    assert "opentrons-emulation/docker/" in service.build.context
    assert service.build.dockerfile == expected_dockerfile_name
    assert get_source_code_build_args(service) == {
        RepoToBuildArgMapping.OPENTRONS.value: opentrons_head
    }


@pytest.mark.parametrize("dev", [True, False])
def test_ot2_emulator_proxy_service_values(
    ot2_system_config: SystemConfigurationModel,
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for EmulatorProxy Service that are specific to OT-2."""
    service = ConcreteEmulatorProxyServiceBuilder(
        ot2_system_config, testing_global_em_config, dev=dev
    ).build_service()

    assert isinstance(service.networks, list)
    assert len(service.networks) == 1
    assert "local-network" in service.networks

    proxy_environment = service.environment
    assert proxy_environment is not None
    assert isinstance(proxy_environment, ListOrDict)
    env_root = cast(Dict[str, Any], proxy_environment.__root__)
    assert env_root is not None
    assert len(env_root.values()) == 4
    assert "OT_EMULATOR_heatershaker_proxy" in env_root
    assert "OT_EMULATOR_magdeck_proxy" in env_root
    assert "OT_EMULATOR_temperature_proxy" in env_root
    assert "OT_EMULATOR_thermocycler_proxy" in env_root

    assert (
        env_root["OT_EMULATOR_heatershaker_proxy"]
        == '{"emulator_port": 10004, "driver_port": 11004}'
    )
    assert (
        env_root["OT_EMULATOR_magdeck_proxy"]
        == '{"emulator_port": 10002, "driver_port": 11002}'
    )
    assert (
        env_root["OT_EMULATOR_temperature_proxy"]
        == '{"emulator_port": 10001, "driver_port": 11001}'
    )
    assert (
        env_root["OT_EMULATOR_thermocycler_proxy"]
        == '{"emulator_port": 10003, "driver_port": 11003}'
    )

    assert service.tty
    assert service.command is None
    assert service.depends_on is None
    assert service.volumes is None


@pytest.mark.parametrize("dev", [True, False])
def test_ot3_emulator_proxy_service_values(
    ot3_system_config: SystemConfigurationModel,
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for EmulatorProxy Service that are specific to OT-3."""
    service = ConcreteEmulatorProxyServiceBuilder(
        ot3_system_config, testing_global_em_config, dev=dev
    ).build_service()

    assert isinstance(service.networks, list)
    assert len(service.networks) == 2
    assert "local-network" in service.networks
    assert "can-network" in service.networks

    proxy_environment = service.environment
    assert proxy_environment is not None
    assert isinstance(proxy_environment, ListOrDict)
    env_root = cast(Dict[str, Any], proxy_environment.__root__)
    assert env_root is not None
    assert len(env_root.values()) == 5
    assert "OT_EMULATOR_heatershaker_proxy" in env_root
    assert "OT_EMULATOR_magdeck_proxy" in env_root
    assert "OT_EMULATOR_temperature_proxy" in env_root
    assert "OT_EMULATOR_thermocycler_proxy" in env_root
    assert "OPENTRONS_PROJECT" in env_root

    assert (
        env_root["OT_EMULATOR_heatershaker_proxy"]
        == '{"emulator_port": 10004, "driver_port": 11004}'
    )
    assert (
        env_root["OT_EMULATOR_magdeck_proxy"]
        == '{"emulator_port": 10002, "driver_port": 11002}'
    )
    assert (
        env_root["OT_EMULATOR_temperature_proxy"]
        == '{"emulator_port": 10001, "driver_port": 11001}'
    )
    assert (
        env_root["OT_EMULATOR_thermocycler_proxy"]
        == '{"emulator_port": 10003, "driver_port": 11003}'
    )
    assert env_root["OPENTRONS_PROJECT"] == "ot3"

    assert service.tty
    assert service.command is None
    assert service.depends_on is None
    assert service.volumes is None
