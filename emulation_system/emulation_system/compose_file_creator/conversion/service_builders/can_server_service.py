"""Module containing CANServerService class."""

from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.images import CANServerImage
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)

from ...input.hardware_models import OT3InputModel
from ...logging import CANServerLoggingClient
from .abstract_service import AbstractService


class CANServerService(AbstractService):
    """Concrete implementation of AbstractService for building a CAN Server."""

    CAN_SERVER_NAME = "can-server"

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Instantiates a CANServerService object."""
        super().__init__(config_model, global_settings, dev)
        self._global_settings = global_settings
        self._logging_client = CANServerLoggingClient(self._dev)
        self._ot3 = self.get_ot3(config_model)
        self._can_image = self._generate_image()

    @staticmethod
    def _generate_image() -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        return CANServerImage().image_name

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

    @property
    def _image(self) -> str:
        return self._can_image

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
        """Check to see if CAN service has established connections to ot3-services."""
        return None

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        return None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        return self._monorepo_source.generate_emulator_mount_strings()

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        ports = self._ot3.get_can_server_bound_port()
        self._logging_client.log_ports(ports)
        return ports

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        env_vars: IntermediateEnvironmentVariables | None = None
        assert isinstance(self._config_model.robot, OT3InputModel)
        if self._config_model.robot.can_server_env_vars is not None:
            env_vars = self._config_model.robot.can_server_env_vars

        self._logging_client.log_env_vars(env_vars)
        return env_vars
