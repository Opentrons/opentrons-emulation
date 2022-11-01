"""Tests to confirm that ConcreteOT3ServiceBuilder builds the CAN Server Service correctly."""
from typing import Any, Dict, List, cast

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.config_file_settings import (
    OT3Hardware,
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.conversion import ServiceBuilderOrchestrator
from emulation_system.compose_file_creator.images import (
    OT3BootloaderImages,
    OT3GantryXImages,
    OT3GantryYImages,
    OT3GripperImages,
    OT3HeadImages,
    OT3PipettesImages,
)
from emulation_system.consts import DEV_DOCKERFILE_NAME, DOCKERFILE_NAME
from tests.compose_file_creator.conversion_logic.conftest import (
    FAKE_COMMIT_ID,
    build_args_are_none,
    get_source_code_build_args,
    partial_string_in_mount,
)


@pytest.fixture
def remote_source_latest(ot3_only: Dict[str, Any]) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    source-type is set to remote.
    source-location is set to latest.
    """
    ot3_only["robot"]["source-type"] = "remote"
    ot3_only["robot"]["source-location"] = "latest"
    ot3_only["robot"]["opentrons-hardware-source-type"] = "remote"
    ot3_only["robot"]["opentrons-hardware-source-location"] = "latest"
    return parse_obj_as(SystemConfigurationModel, ot3_only)


@pytest.fixture
def remote_source_commit_id(ot3_only: Dict[str, Any]) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    source-type is set to remote.
    source-location is set a commit id.
    """
    ot3_only["robot"]["source-type"] = "remote"
    ot3_only["robot"]["source-location"] = FAKE_COMMIT_ID
    ot3_only["robot"]["opentrons-hardware-source-type"] = "remote"
    ot3_only["robot"]["opentrons-hardware-source-location"] = FAKE_COMMIT_ID
    return parse_obj_as(SystemConfigurationModel, ot3_only)


@pytest.fixture
def local_source(
    ot3_only: Dict[str, Any], ot3_firmware_dir: str, opentrons_dir: str
) -> SystemConfigurationModel:
    """Gets SystemConfigurationModel.

    source-type is set to local.
    source-location is set to a monorepo dir.
    """
    ot3_only["robot"]["source-type"] = "local"
    ot3_only["robot"]["source-location"] = ot3_firmware_dir
    ot3_only["robot"]["opentrons-hardware-source-type"] = "local"
    ot3_only["robot"]["opentrons-hardware-source-location"] = opentrons_dir

    return parse_obj_as(SystemConfigurationModel, ot3_only)


def get_ot3_service(service_list: List[Service], hardware: OT3Hardware) -> Service:
    """Load OT-3 Service from passed service_list."""
    for service in service_list:
        assert service.image is not None
        if hardware in service.image:
            return service

    raise Exception(f"Service with hardware {hardware} not found.")


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
def test_simple_ot3_values(
    config_model: SystemConfigurationModel,
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for values that are the same for all configurations of a Smoothie Service."""
    services = ServiceBuilderOrchestrator(
        config_model, testing_global_em_config, dev
    )._build_ot3_services(
        can_server_service_name="can-server", state_manager_name="state-manager"
    )

    expected_dockerfile_name = DEV_DOCKERFILE_NAME if dev else DOCKERFILE_NAME

    for service in services:
        assert isinstance(service.build, BuildItem)
        assert service.build.dockerfile == expected_dockerfile_name
        assert isinstance(service.build.context, str)
        assert "opentrons-emulation/docker/" in service.build.context
        assert isinstance(service.networks, list)
        assert len(service.networks) == 2
        assert "local-network" in service.networks
        assert "can-network" in service.networks
        assert service.tty
        assert service.command is None
        assert service.depends_on is None


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
def test_ot3_service_container_names_values(
    config_model: SystemConfigurationModel,
    dev: bool,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for container name for all configurations of a Smoothie Service."""
    services = ServiceBuilderOrchestrator(
        config_model, testing_global_em_config, dev
    )._build_ot3_services(
        can_server_service_name="can-server", state_manager_name="state-manager"
    )

    # The number of items in ServiceBuilderOrchestrator.OT3_SERVICES_TO_CREATE
    assert len(services) == 6
    head = get_ot3_service(services, OT3Hardware.HEAD)
    pipettes = get_ot3_service(services, OT3Hardware.PIPETTES)
    gantry_x = get_ot3_service(services, OT3Hardware.GANTRY_X)
    gantry_y = get_ot3_service(services, OT3Hardware.GANTRY_Y)
    bootloader = get_ot3_service(services, OT3Hardware.BOOTLOADER)
    gripper = get_ot3_service(services, OT3Hardware.GRIPPER)

    assert head.container_name == OT3Hardware.HEAD
    assert pipettes.container_name == OT3Hardware.PIPETTES
    assert gantry_x.container_name == OT3Hardware.GANTRY_X
    assert gantry_y.container_name == OT3Hardware.GANTRY_Y
    assert bootloader.container_name == OT3Hardware.BOOTLOADER
    assert gripper.container_name == OT3Hardware.GRIPPER


@pytest.mark.parametrize(
    "config_model",
    [
        lazy_fixture("remote_source_latest"),
        lazy_fixture("remote_source_commit_id"),
        lazy_fixture("local_source"),
    ],
)
def test_ot3_service_environment_variables(
    config_model: SystemConfigurationModel,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Tests for values that are the same for all configurations of a Smoothie Service."""
    services = ServiceBuilderOrchestrator(
        config_model, testing_global_em_config, dev=True
    )._build_ot3_services(
        can_server_service_name="can-server", state_manager_name="state-manager"
    )

    # The number of items in ServiceBuilderOrchestrator.OT3_SERVICES_TO_CREATE
    assert len(services) == 6
    head = get_ot3_service(services, OT3Hardware.HEAD)
    gantry_x = get_ot3_service(services, OT3Hardware.GANTRY_X)
    gantry_y = get_ot3_service(services, OT3Hardware.GANTRY_Y)
    bootloader = get_ot3_service(services, OT3Hardware.BOOTLOADER)
    gripper = get_ot3_service(services, OT3Hardware.GRIPPER)
    pipettes = get_ot3_service(services, OT3Hardware.PIPETTES)

    not_pipette_or_gripper_services = [head, gantry_x, gantry_y]

    for service in not_pipette_or_gripper_services:
        service_env = service.environment
        assert service_env is not None
        env_root = cast(Dict[str, Any], service_env.__root__)
        assert env_root is not None
        assert len(env_root.values()) == 3
        assert "CAN_SERVER_HOST" in env_root
        assert "STATE_MANAGER_HOST" in env_root
        assert "STATE_MANAGER_PORT" in env_root

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

    bootloader_service_env = bootloader.environment
    assert bootloader_service_env is not None
    bootloader_env_root = cast(Dict[str, Any], bootloader_service_env.__root__)
    assert len(bootloader_env_root.values()) == 1
    assert "CAN_SERVER_HOST" in env_root


@pytest.mark.parametrize(
    "config_model, expected_firmware_url, expected_monorepo_url",
    [
        (
            lazy_fixture("remote_source_latest"),
            lazy_fixture("ot3_firmware_head"),
            lazy_fixture("opentrons_head"),
        ),
        (
            lazy_fixture("remote_source_commit_id"),
            lazy_fixture("ot3_firmware_commit"),
            lazy_fixture("opentrons_commit"),
        ),
    ],
)
def test_ot3_service_remote(
    config_model: SystemConfigurationModel,
    testing_global_em_config: OpentronsEmulationConfiguration,
    expected_firmware_url: str,
    expected_monorepo_url: str,
) -> None:
    """Tests for values that are the same for all remote configurations of a Smoothie Service."""
    services = ServiceBuilderOrchestrator(
        config_model, testing_global_em_config, dev=True
    )._build_ot3_services(
        can_server_service_name="can-server", state_manager_name="state-manager"
    )
    assert len(services) == 6
    head = get_ot3_service(services, OT3Hardware.HEAD)
    pipettes = get_ot3_service(services, OT3Hardware.PIPETTES)
    gantry_x = get_ot3_service(services, OT3Hardware.GANTRY_X)
    gantry_y = get_ot3_service(services, OT3Hardware.GANTRY_Y)
    bootloader = get_ot3_service(services, OT3Hardware.BOOTLOADER)
    gripper = get_ot3_service(services, OT3Hardware.GRIPPER)

    assert head.image == OT3HeadImages().remote_hardware_image_name
    assert pipettes.image == OT3PipettesImages().remote_hardware_image_name
    assert gantry_x.image == OT3GantryXImages().remote_hardware_image_name
    assert gantry_y.image == OT3GantryYImages().remote_hardware_image_name
    assert bootloader.image == OT3BootloaderImages().remote_hardware_image_name
    assert gripper.image == OT3GripperImages().remote_hardware_image_name

    assert isinstance(head.build, BuildItem)
    assert isinstance(pipettes.build, BuildItem)
    assert isinstance(gantry_x.build, BuildItem)
    assert isinstance(gantry_y.build, BuildItem)
    assert isinstance(bootloader.build, BuildItem)
    assert isinstance(gripper.build, BuildItem)

    assert head.build.target == OT3HeadImages().remote_hardware_image_name
    assert pipettes.build.target == OT3PipettesImages().remote_hardware_image_name
    assert gantry_x.build.target == OT3GantryXImages().remote_hardware_image_name
    assert gantry_y.build.target == OT3GantryYImages().remote_hardware_image_name
    assert bootloader.build.target == OT3BootloaderImages().remote_hardware_image_name
    assert gripper.build.target == OT3GripperImages().remote_hardware_image_name

    for service in services:
        build_args = get_source_code_build_args(service)
        ot3_firmware_build_arg = RepoToBuildArgMapping.OT3_FIRMWARE
        monorepo_build_arg = RepoToBuildArgMapping.OPENTRONS

        assert ot3_firmware_build_arg in build_args
        assert monorepo_build_arg in build_args
        assert build_args[ot3_firmware_build_arg] == expected_firmware_url
        assert build_args[monorepo_build_arg] == expected_monorepo_url
        assert service.volumes is None


def test_ot3_services_local(
    local_source: SystemConfigurationModel,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Test for values for local configuration of a Smoothie Service."""
    services = ServiceBuilderOrchestrator(
        local_source, testing_global_em_config, dev=True
    )._build_ot3_services(
        can_server_service_name="can-server", state_manager_name="state-manager"
    )
    assert len(services) == 6
    head = get_ot3_service(services, OT3Hardware.HEAD)
    pipettes = get_ot3_service(services, OT3Hardware.PIPETTES)
    gantry_x = get_ot3_service(services, OT3Hardware.GANTRY_X)
    gantry_y = get_ot3_service(services, OT3Hardware.GANTRY_Y)
    bootloader = get_ot3_service(services, OT3Hardware.BOOTLOADER)
    gripper = get_ot3_service(services, OT3Hardware.GRIPPER)

    assert head.image == OT3HeadImages().local_hardware_image_name
    assert pipettes.image == OT3PipettesImages().local_hardware_image_name
    assert gantry_x.image == OT3GantryXImages().local_hardware_image_name
    assert gantry_y.image == OT3GantryYImages().local_hardware_image_name
    assert bootloader.image == OT3BootloaderImages().local_hardware_image_name
    assert gripper.image == OT3GripperImages().local_hardware_image_name

    assert isinstance(head.build, BuildItem)
    assert isinstance(pipettes.build, BuildItem)
    assert isinstance(gantry_x.build, BuildItem)
    assert isinstance(gantry_y.build, BuildItem)
    assert isinstance(bootloader.build, BuildItem)
    assert isinstance(gripper.build, BuildItem)

    assert head.build.target == OT3HeadImages().local_hardware_image_name
    assert pipettes.build.target == OT3PipettesImages().local_hardware_image_name
    assert gantry_x.build.target == OT3GantryXImages().local_hardware_image_name
    assert gantry_y.build.target == OT3GantryYImages().local_hardware_image_name
    assert bootloader.build.target == OT3BootloaderImages().local_hardware_image_name
    assert gripper.build.target == OT3GripperImages().local_hardware_image_name

    for service in services:
        assert build_args_are_none(service)
        volumes = service.volumes
        assert volumes is not None
        assert len(volumes) == 6
        assert partial_string_in_mount("ot3-firmware:/ot3-firmware", volumes)
        assert partial_string_in_mount("entrypoint.sh:/entrypoint.sh", volumes)
        assert partial_string_in_mount(
            "ot3-firmware-build-host:/ot3-firmware/build-host", volumes
        )
        assert partial_string_in_mount(
            "ot3-firmware-stm32-tools:/ot3-firmware/stm32-tools", volumes
        )

        assert partial_string_in_mount("opentrons:/opentrons", volumes)
        assert partial_string_in_mount("opentrons-python-dist:/dist", volumes)
