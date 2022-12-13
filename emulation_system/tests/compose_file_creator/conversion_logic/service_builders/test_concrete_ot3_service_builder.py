"""Tests to confirm that ConcreteOT3ServiceBuilder builds the CAN Server Service correctly."""
from typing import (
    Any,
    Dict,
    List,
    cast,
)

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import (
    OpentronsEmulationConfiguration,
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator import (
    BuildItem,
    Service,
)
from emulation_system.compose_file_creator.config_file_settings import (
    OT3Hardware,
)
from emulation_system.compose_file_creator.conversion import ServiceBuilderOrchestrator
from emulation_system.consts import (
    DEV_DOCKERFILE_NAME,
    DOCKERFILE_NAME,
)
from tests.compose_file_creator.conversion_logic.conftest import (
    build_args_are_none,
    partial_string_in_mount,
)


def get_ot3_service(service_list: List[Service], hardware: OT3Hardware) -> Service:
    """Load OT-3 Service from passed service_list."""
    for service in service_list:
        assert service.image is not None
        if hardware in service.image:
            return service

    raise Exception(f"Service with hardware {hardware} not found.")


@pytest.mark.parametrize(
    "model_dict, dev",
    [
        (lazy_fixture("ot3_only"), True),
        (lazy_fixture("ot3_only"), False),
        (lazy_fixture("ot3_remote_everything_commit_id"), True),
        (lazy_fixture("ot3_remote_everything_commit_id"), False),
        (lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"), True),
        (lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"), False),
        (lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"), True),
        (lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"), False),
        (lazy_fixture("ot3_local_everything"), True),
        (lazy_fixture("ot3_local_everything"), False),
    ],
)
def test_simple_ot3_values(
    model_dict: Dict[str, Any],
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for values that are the same for all configurations of a Smoothie Service."""
    config_model = parse_obj_as(SystemConfigurationModel, model_dict)
    services = ServiceBuilderOrchestrator(
        config_model, testing_global_em_config, dev
    )._build_ot3_services(
        can_server_service_name="can-server", state_manager_name="state-manager"
    )
    head = get_ot3_service(services, OT3Hardware.HEAD)
    pipettes = get_ot3_service(services, OT3Hardware.PIPETTES)
    gantry_x = get_ot3_service(services, OT3Hardware.GANTRY_X)
    gantry_y = get_ot3_service(services, OT3Hardware.GANTRY_Y)
    bootloader = get_ot3_service(services, OT3Hardware.BOOTLOADER)
    gripper = get_ot3_service(services, OT3Hardware.GRIPPER)

    expected_dockerfile_name = DEV_DOCKERFILE_NAME if dev else DOCKERFILE_NAME
    assert len(services) == 6

    for service in services:
        # Build
        assert isinstance(service.build, BuildItem)
        assert service.build.dockerfile == expected_dockerfile_name
        assert isinstance(service.build.context, str)
        assert "opentrons-emulation/docker/" in service.build.context
        assert build_args_are_none(service)

        # Networks
        assert isinstance(service.networks, list)
        assert len(service.networks) == 2
        assert "local-network" in service.networks
        assert "can-network" in service.networks

        # Volumes
        volumes = service.volumes
        assert volumes is not None
        assert len(volumes) == 3
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", service)
        assert partial_string_in_mount("state_manager_venv:/ot3-firmware/build-host/.venv", service)
        assert partial_string_in_mount("_executable:/executable", service)

        # Misc
        assert service.tty
        assert service.command is None
        assert service.depends_on is None

    # Container Names
    assert head.container_name == OT3Hardware.HEAD
    assert pipettes.container_name == OT3Hardware.PIPETTES
    assert gantry_x.container_name == OT3Hardware.GANTRY_X
    assert gantry_y.container_name == OT3Hardware.GANTRY_Y
    assert bootloader.container_name == OT3Hardware.BOOTLOADER
    assert gripper.container_name == OT3Hardware.GRIPPER

    not_pipette_or_gripper_services = [head, gantry_x, gantry_y]

    # Env vars 1/3

    for service in not_pipette_or_gripper_services:
        service_env = service.environment
        assert service_env is not None
        env_root = cast(Dict[str, Any], service_env.__root__)
        assert env_root is not None
        assert len(env_root.values()) == 3
        assert "CAN_SERVER_HOST" in env_root
        assert "STATE_MANAGER_HOST" in env_root
        assert "STATE_MANAGER_PORT" in env_root

    # Env vars 2/3
    for service in [pipettes, gripper]:
        service_env = service.environment
        assert service_env is not None
        env_root = cast(Dict[str, Any], service_env.__root__)
        assert env_root is not None
        assert len(env_root.values()) == 4
        assert "CAN_SERVER_HOST" in env_root
        assert "EEPROM_FILENAME" in env_root
        assert "STATE_MANAGER_HOST" in env_root
        assert "STATE_MANAGER_PORT" in env_root

    # Env vars 3/3
    bootloader_service_env = bootloader.environment
    assert bootloader_service_env is not None
    bootloader_env_root = cast(Dict[str, Any], bootloader_service_env.__root__)
    assert len(bootloader_env_root.values()) == 1
    assert "CAN_SERVER_HOST" in env_root
