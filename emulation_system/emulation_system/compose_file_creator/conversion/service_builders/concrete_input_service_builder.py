"""Module containing ConcreteInputServiceBuilder."""
from typing import Any, Dict, List, Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.compose_file_creator.utilities.shared_functions import (
    add_opentrons_modules_named_volumes,
    add_opentrons_named_volumes,
    add_ot3_firmware_named_volumes,
    get_build_args,
)

from ...config_file_settings import OpentronsRepository
from ...types.input_types import Containers
from ...utilities.hardware_utils import (
    is_hardware_emulation_level,
    is_module,
    is_ot2,
    is_ot3,
    is_remote_module,
    is_remote_robot,
    is_robot,
)
from .abstract_service_builder import AbstractServiceBuilder


class ConcreteInputServiceBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building an Input Service."""

    SMOOTHIE_NAME = "smoothie"

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
        container: Containers,
        emulator_proxy_name: Optional[str],
        smoothie_name: Optional[str],
        can_server_service_name: Optional[str],
    ) -> None:
        """Instantiates a ConcreteInputServiceBuilder object."""
        super().__init__(config_model, global_settings)
        self._container = container
        self._emulator_proxy_name = emulator_proxy_name
        self._smoothie_name = smoothie_name
        self._can_server_service_name = can_server_service_name
        self._dev = dev
        self._image = self._generate_image()

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        return self._container.get_image_name()

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self._container.id, system_unique_id
        )
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return f"{self._image}:latest"

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        tty = True
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        networks = self._config_model.required_networks
        return networks

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        build_args = None
        source_location = None
        if is_remote_robot(self._container):
            source_location = self._container.robot_server_source_location
        elif is_remote_module(self._container):
            source_location = self._container.source_location

        if source_location is not None:
            repo = self._container.get_source_repo()
            build_args = get_build_args(
                repo,
                source_location,
                self._global_settings.get_repo_commit(repo),
                self._global_settings.get_repo_head(repo),
            )
        return build_args

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        mount_strings: List[str] = (
            self._container.get_robot_server_mount_strings()
            if is_robot(self._container)
            else self._container.get_mount_strings()
        )
        if len(mount_strings) > 0:
            mount_strings.append(self.ENTRYPOINT_MOUNT_STRING)
            source_repo = self._container.get_source_repo()
            match source_repo:
                case OpentronsRepository.OPENTRONS:
                    add_opentrons_named_volumes(mount_strings)
                case OpentronsRepository.OPENTRONS_MODULES:
                    add_opentrons_modules_named_volumes(mount_strings)
                case OpentronsRepository.OT3_FIRMWARE:
                    add_ot3_firmware_named_volumes(mount_strings)
            return mount_strings
        else:
            return None

    def generate_command(self) -> Optional[IntermediateCommand]:
        """Generates value for command parameter."""
        command = None
        if self._emulator_proxy_name is not None:
            command = (
                self._container.get_hardware_level_command(self._emulator_proxy_name)
                if is_hardware_emulation_level(self._container)
                else self._container.get_firmware_level_command(
                    self._emulator_proxy_name
                )
            )

        return command

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        return (
            [self._container.get_port_binding_string()]
            if is_robot(self._container)
            else None
        )

    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        """Generates value for depends_on parameter."""
        dependencies = []
        if self._emulator_proxy_name is not None:
            dependencies.append(self._emulator_proxy_name)

        if self._smoothie_name is not None and is_ot2(self._container):
            dependencies.append(self._smoothie_name)

        return dependencies if len(dependencies) != 0 else None

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        temp_vars: Dict[str, Any] = {}

        if is_robot(self._container) and self._emulator_proxy_name is not None:
            temp_vars[
                "OT_EMULATOR_module_server"
            ] = f'{{"host": "{self._emulator_proxy_name}"}}'

        if is_ot2(self._container):
            # TODO: If emulator proxy port is ever not hardcoded will have to update from
            #  11000 to a variable
            temp_vars[
                "OT_SMOOTHIE_EMULATOR_URI"
            ] = f"socket://{self._smoothie_name}:11000"

        if is_ot3(self._container):
            temp_vars["OT_API_FF_enableOT3HardwareController"] = True
            temp_vars["OT3_CAN_DRIVER_interface"] = "opentrons_sock"
            temp_vars["OT3_CAN_DRIVER_host"] = self._can_server_service_name
            temp_vars["OT3_CAN_DRIVER_port"] = 9898

        if is_module(self._container):
            temp_vars.update(self._container.get_serial_number_env_var())
            temp_vars.update(self._container.get_proxy_info_env_var())
        return temp_vars
