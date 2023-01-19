import os
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
)

import docker
import pytest
import yaml
from docker.models.containers import Container

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.conversion.conversion_functions import convert_from_obj
from emulation_system.compose_file_creator.output.runtime_compose_file_model import RuntimeComposeFileModel
from emulation_system.consts import ROOT_DIR


@dataclass
class OT3System:
    """Dataclass to access all containers in OT-3 System easily."""
    gantry_x_name: str
    gantry_y_name: str
    head_name: str
    gripper_name: str
    pipettes_name: str
    bootloader_name: str
    state_manager_name: str
    robot_server_name: str
    can_server_name: str
    emulator_proxy_name: str
    firmware_builder_name: str
    monorepo_builder_name: str
    modules_builder_name: Optional[str]


def get_volumes(container: Container) -> Optional[List[Dict[str, Any]]]:
    return [
        mount
        for mount
        in docker.from_env().api.inspect_container(container)["Mounts"]
        if mount["Type"] == "volume"
    ]


def get_mounts(container: Container) -> Optional[List[Dict[str, Any]]]:
    return [
        mount
        for mount
        in docker.from_env().api.inspect_container(container)["Mounts"]
        if mount["Type"] == "bind"
    ]


def get_container_name(service: Service) -> Optional[str]:
    if service is None:
        return
    else:
        return service.container_name


@pytest.fixture
def model_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    def _model_under_test(relative_path: str) -> OT3System:
        abs_path = os.path.join(ROOT_DIR, relative_path)
        with open(abs_path, "r") as file:
            contents = yaml.safe_load(file)
        system: RuntimeComposeFileModel = convert_from_obj(
            contents,
            testing_global_em_config,
            False
        )

        return OT3System(
            gantry_x_name=get_container_name(system.ot3_gantry_x_emulator),
            gantry_y_name=get_container_name(system.ot3_gantry_y_emulator),
            head_name=get_container_name(system.ot3_head_emulator),
            gripper_name=get_container_name(system.ot3_gripper_emulator),
            pipettes_name=get_container_name(system.ot3_pipette_emulator),
            bootloader_name=get_container_name(system.ot3_bootloader_emulator),
            state_manager_name=get_container_name(system.ot3_state_manager),
            robot_server_name=get_container_name(system.robot_server),
            can_server_name=get_container_name(system.can_server),
            emulator_proxy_name=get_container_name(system.emulator_proxy),
            firmware_builder_name=get_container_name(system.ot3_firmware_builder),
            monorepo_builder_name=get_container_name(system.monorepo_builder),
            modules_builder_name=get_container_name(system.opentrons_modules_builder),
        )

    return _model_under_test


@pytest.fixture
def ot3_only_system(model_under_test: Callable) -> OT3System:
    return model_under_test(
        relative_path="samples/common_use_cases/basic/ot3_only.yaml"
    )


def test_ot3_only_system(ot3_only_system: OT3System) -> None:
    print(ot3_only_system)
    monorepo_builder_vols = get_volumes(ot3_only_system.monorepo_builder_name)
    assert monorepo_builder_vols is not None
