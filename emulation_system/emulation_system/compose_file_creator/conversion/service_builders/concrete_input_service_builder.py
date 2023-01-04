"""Module containing ConcreteInputServiceBuilder."""
from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.source import Source

from ...config_file_settings import OpentronsRepository
from ...logging import InputLoggingClient
from ...types.input_types import Containers
from ...utilities.conversion_utils import get_input_container_source
from ...utilities.hardware_utils import is_module, is_ot2, is_ot3, is_robot
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
        super().__init__(config_model, global_settings, dev)
        self._container = container
        self._emulator_proxy_name = emulator_proxy_name
        self._smoothie_name = smoothie_name
        self._can_server_service_name = can_server_service_name
        self._container_name = self._internal_generate_container_name()
        self._logging_client = InputLoggingClient(self._container_name, self._dev)
        self._input_image = self._generate_image()
        self._logging_client.log_container_name(
            self._container.id,
            self._container_name,
            self._config_model.system_unique_id,
        )

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        image_name = self._container.get_image_name()

        # self._logging_client.log_image_name(image_name, source_type, "source-type")
        return image_name

    def _internal_generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self._container.id, system_unique_id
        )
        return container_name

    def generate_container_name(self) -> str:
        """Return container name."""
        return self._container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return self._image

    @property
    def _image(self) -> str:
        return self._input_image

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        tty = True
        self._logging_client.log_tty(tty)
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        networks = self._config_model.required_networks
        self._logging_client.log_networks(networks)
        return networks

    def generate_healthcheck(self) -> Optional[IntermediateHealthcheck]:
        """Healthcheck generate for all input services."""
        return None

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        return None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        source: Source = get_input_container_source(self._container, self._config_model)
        volumes = []

        if source.repo == OpentronsRepository.OPENTRONS or is_robot(self._container):
            volumes.extend(self._monorepo_source.generate_emulator_mount_strings())
        elif source.repo == OpentronsRepository.OPENTRONS_MODULES:
            volumes.extend(
                self._opentrons_modules_source.generate_emulator_mount_strings_from_hw(
                    self._container.hardware
                )
            )

        self._logging_client.log_volumes(volumes)
        return volumes

    def generate_command(self) -> Optional[IntermediateCommand]:
        """Generates value for command parameter."""
        command = None
        if self._emulator_proxy_name is not None:
            command = (
                self._container.get_hardware_level_command(self._emulator_proxy_name)
                if self._container.is_hardware_emulation_level()
                else self._container.get_firmware_level_command(
                    self._emulator_proxy_name
                )
            )
        self._logging_client.log_command(command)
        return command

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        ports = (
            [self._container.get_port_binding_string()]
            if is_robot(self._container)
            else None
        )
        self._logging_client.log_ports(ports)
        return ports

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        temp_vars: IntermediateEnvironmentVariables = {}

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
            assert self._can_server_service_name is not None
            temp_vars["OT_API_FF_enableOT3HardwareController"] = True
            temp_vars["OT3_CAN_DRIVER_interface"] = "opentrons_sock"
            temp_vars["OT3_CAN_DRIVER_host"] = self._can_server_service_name
            temp_vars["OT3_CAN_DRIVER_port"] = self.get_ot3(
                self._config_model
            ).can_server_bound_port

        if (
            is_ot3(self._container) or is_ot2(self._container)
        ) and self._container.robot_server_env_vars is not None:
            temp_vars.update(self._container.robot_server_env_vars)

        if is_module(self._container):
            temp_vars.update(self._container.get_serial_number_env_var())
            temp_vars.update(self._container.get_proxy_info_env_var())

        if is_module(self._container) and self._container.module_env_vars is not None:
            temp_vars.update(self._container.module_env_vars)

        env_vars = None if len(temp_vars) == 0 else temp_vars
        self._logging_client.log_env_vars(env_vars)
        return env_vars
