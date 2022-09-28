"""Module containing ConcreteCANServerServiceBuilder class."""

from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.images import CANServerImages
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.compose_file_creator.utilities.shared_functions import (
    add_opentrons_named_volumes,
    get_build_args,
    get_entrypoint_mount_string,
    get_service_build,
)

from ...logging import CANServerLoggingClient
from .abstract_service_builder import AbstractServiceBuilder


class ConcreteCANServerServiceBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building a CAN Server."""

    CAN_SERVER_NAME = "can-server"

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Instantiates a ConcreteCANServerServiceBuilder object."""
        super().__init__(config_model, global_settings)
        self._dev = dev
        self._logging_client = CANServerLoggingClient(self._dev)
        self._ot3 = self.get_ot3(config_model)
        self._image = self._generate_image()

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        source_type = self._ot3.can_server_source_type
        image_name = (
            CANServerImages().local_firmware_image_name
            if source_type == SourceType.LOCAL
            else CANServerImages().remote_firmware_image_name
        )
        self._logging_client.log_image_name(
            image_name, source_type, "can-server-source-type"
        )
        return image_name

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self.CAN_SERVER_NAME, system_unique_id
        )
        self._logging_client.log_container_name(
            self.CAN_SERVER_NAME, container_name, system_unique_id
        )
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return self._image

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

    def generate_build(self) -> Optional[BuildItem]:
        """Generates value for build parameter."""
        repo = OpentronsRepository.OPENTRONS
        if self._ot3.can_server_source_type == SourceType.REMOTE:
            build_args = get_build_args(
                repo,
                self._ot3.can_server_source_location,
                self._global_settings.get_repo_commit(repo),
                self._global_settings.get_repo_head(repo),
            )

        else:
            build_args = None
        self._logging_client.log_build_args(build_args)
        return get_service_build(self._image, build_args, self._dev)

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        if self._ot3.can_server_source_type == SourceType.LOCAL:
            volumes = [get_entrypoint_mount_string()]
            volumes.extend(self._ot3.get_can_mount_strings())
            add_opentrons_named_volumes(volumes)
        else:
            volumes = None
        self._logging_client.log_volumes(volumes)
        return volumes

    def generate_command(self) -> Optional[IntermediateCommand]:
        """Generates value for command parameter."""
        command = None
        self._logging_client.log_command(command)
        return command

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        ports = self._ot3.get_can_server_bound_port()
        self._logging_client.log_ports(ports)
        return ports

    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        """Generates value for depends_on parameter."""
        depends_on = None
        self._logging_client.log_depends_on(depends_on)
        return depends_on

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        env_vars = None
        self._logging_client.log_env_vars(env_vars)
        return env_vars
