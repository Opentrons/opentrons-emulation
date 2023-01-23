import os
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional

import docker
import pytest
import yaml
from docker.models.containers import Container

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.config_file_settings import (
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.consts import COMMIT_SHA_REGEX, ROOT_DIR


@dataclass
class OT3System:
    """Dataclass to access all containers in OT-3 System easily."""

    gantry_x: Container
    gantry_y: Container
    head: Container
    gripper: Container
    pipettes: Container
    bootloader: Container
    state_manager: Container
    robot_server: Container
    can_server: Container
    emulator_proxy: Container

    # firmware and monorepo will actually always exist
    # but want to check that with an assert and not a type error
    firmware_builder: Optional[Container]
    monorepo_builder: Optional[Container]
    modules_builder: Optional[Container]

    def _parse_build_args(
        self, container: Container, head_ref: str, build_arg_name: str
    ) -> "BuildArgConfigurations":
        if container is None:
            return BuildArgConfigurations.NO_BUILD_ARGS

        monorepo_env_dict = self._convert_env_list_to_dict(container)
        if build_arg_name not in monorepo_env_dict.keys():
            return BuildArgConfigurations.NO_BUILD_ARGS

        build_arg_state: BuildArgConfigurations
        build_arg_val = monorepo_env_dict[build_arg_name]

        if build_arg_val.endswith(head_ref):
            build_arg_state = BuildArgConfigurations.LATEST_BUILD_ARGS
        elif re.search(COMMIT_SHA_REGEX, build_arg_val) is not None:
            build_arg_state = BuildArgConfigurations.COMMIT_ID_BUILD_ARGS
        else:
            raise ValueError("Build arg did not match anything.")

        return build_arg_state

    @staticmethod
    def _convert_env_list_to_dict(container: Container) -> Dict[str, str]:
        return dict(
            [env_val.split("=", 1) for env_val in container.attrs["Config"]["Env"]]
        )

    @property
    def monorepo_builder_created(self) -> bool:
        return self.monorepo_builder is not None

    @property
    def local_monorepo_mounted(self) -> bool:
        if self.monorepo_builder is None:
            return False

        monorepo_builder_mounts = get_mounts(self.monorepo_builder)
        return self.monorepo_builder_created and any(
            mount["Destination"] == "/opentrons" for mount in monorepo_builder_mounts
        )

    @property
    def monorepo_build_args(self) -> "BuildArgConfigurations":
        return self._parse_build_args(
            self.monorepo_builder,
            "opentrons/archive/refs/heads/edge.zip",
            RepoToBuildArgMapping.OPENTRONS,
        )

    @property
    def ot3_firmware_builder_created(self) -> bool:
        return self.firmware_builder is not None

    @property
    def local_ot3_firmware_mounted(self) -> bool:
        if self.firmware_builder is None:
            return False

        firmware_builder_mounts = get_mounts(self.firmware_builder)
        return self.ot3_firmware_builder_created and any(
            mount["Destination"] == "/ot3-firmware" for mount in firmware_builder_mounts
        )

    @property
    def ot3_firmware_build_args(self) -> "BuildArgConfigurations":
        return self._parse_build_args(
            self.firmware_builder,
            "ot3-firmware/archive/refs/heads/main.zip",
            RepoToBuildArgMapping.OT3_FIRMWARE,
        )

    @property
    def opentrons_modules_builder_created(self) -> bool:
        return self.modules_builder is not None

    @property
    def local_opentrons_modules_mounted(self) -> bool:
        if self.modules_builder is None:
            return False

        modules_builder_mounts = get_mounts(self.modules_builder)
        return self.opentrons_modules_builder_created and any(
            mount["Destination"] == "/opentrons-modules"
            for mount in modules_builder_mounts
        )

    @property
    def opentrons_modules_build_args(self) -> "BuildArgConfigurations":
        return self._parse_build_args(
            self.modules_builder,
            "opentrons-modules/archive/refs/heads/edge.zip",
            RepoToBuildArgMapping.OPENTRONS_MODULES,
        )


class BuildArgConfigurations(Enum):
    NO_BUILD_ARGS = auto()
    LATEST_BUILD_ARGS = auto()
    COMMIT_ID_BUILD_ARGS = auto()


@dataclass
class OT3SystemValidationModel:
    monorepo_builder_created: bool
    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool

    local_monorepo_mounted: bool
    local_ot3_firmware_mounted: bool
    local_opentrons_modules_mounted: bool

    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations

    def _check_monorepo_named_volumes(self, container: Container) -> None:
        volumes = get_volumes(container)
        assert volumes is not None
        assert (
            len(
                [
                    volume
                    for volume in volumes
                    if (
                        volume["Type"] == "volume"
                        and volume["Name"] == "monorepo-wheels"
                        and volume["Destination"] == "/dist"
                    )
                ]
            )
            == 1
        )

    def compare(self, ot3_system: OT3System) -> None:
        assert ot3_system.monorepo_builder_created == self.monorepo_builder_created
        assert (
            ot3_system.ot3_firmware_builder_created == self.ot3_firmware_builder_created
        )
        assert (
            ot3_system.opentrons_modules_builder_created
            == self.opentrons_modules_builder_created
        )

        assert ot3_system.local_monorepo_mounted == self.local_monorepo_mounted
        assert ot3_system.local_ot3_firmware_mounted == self.local_ot3_firmware_mounted
        assert (
            ot3_system.local_opentrons_modules_mounted
            == self.local_opentrons_modules_mounted
        )
        assert ot3_system.monorepo_build_args == self.monorepo_build_args
        assert ot3_system.ot3_firmware_build_args == self.ot3_firmware_build_args
        assert (
            ot3_system.opentrons_modules_build_args == self.opentrons_modules_build_args
        )

        if self.monorepo_builder_created:
            self._check_monorepo_named_volumes(ot3_system.monorepo_builder)


def get_volumes(container: Container) -> Optional[List[Dict[str, Any]]]:
    return [mount for mount in container.attrs["Mounts"] if mount["Type"] == "volume"]


def get_mounts(container: Container) -> Optional[List[Dict[str, Any]]]:
    return [mount for mount in container.attrs["Mounts"] if mount["Type"] == "bind"]


def get_container(service: Service) -> Optional[Container]:
    if service is None:
        return
    else:
        return docker.from_env().containers.get(service.container_name)


@pytest.fixture
def model_under_test(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    def _model_under_test(relative_path: str) -> OT3System:
        abs_path = os.path.join(ROOT_DIR, relative_path)
        with open(abs_path, "r") as file:
            contents = yaml.safe_load(file)
        system: RuntimeComposeFileModel = convert_from_obj(
            contents, testing_global_em_config, False
        )

        return OT3System(
            gantry_x=get_container(system.ot3_gantry_x_emulator),
            gantry_y=get_container(system.ot3_gantry_y_emulator),
            head=get_container(system.ot3_head_emulator),
            gripper=get_container(system.ot3_gripper_emulator),
            pipettes=get_container(system.ot3_pipette_emulator),
            bootloader=get_container(system.ot3_bootloader_emulator),
            state_manager=get_container(system.ot3_state_manager),
            robot_server=get_container(system.robot_server),
            can_server=get_container(system.can_server),
            emulator_proxy=get_container(system.emulator_proxy),
            firmware_builder=get_container(system.ot3_firmware_builder),
            monorepo_builder=get_container(system.monorepo_builder),
            modules_builder=get_container(system.opentrons_modules_builder),
        )

    return _model_under_test
