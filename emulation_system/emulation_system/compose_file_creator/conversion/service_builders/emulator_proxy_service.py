"""Module containing EmulatorProxyService class."""

from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    RobotInputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)

from ...images import EmulatorProxyImage
from ...logging import EmulatorProxyLoggingClient
from .abstract_service import AbstractService


class EmulatorProxyService(AbstractService):
    """Concrete implementation of AbstractService for building an Emulator Proxy."""

    EMULATOR_PROXY_NAME = "emulator-proxy"

    MODULE_TYPES = [
        ThermocyclerModuleInputModel,
        TemperatureModuleInputModel,
        HeaterShakerModuleInputModel,
        MagneticModuleInputModel,
    ]

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Instantiates a EmulatorProxyService object."""
        super().__init__(config_model, global_settings, dev)
        self._logging_client = EmulatorProxyLoggingClient(self._dev)
        self._emulator_image = self._generate_image()

    @staticmethod
    def _generate_image() -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        return EmulatorProxyImage().image_name

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self.EMULATOR_PROXY_NAME, system_unique_id
        )
        self._logging_client.log_container_name(
            self.EMULATOR_PROXY_NAME, container_name, system_unique_id
        )
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return self._image

    @property
    def _image(self) -> str:
        return self._emulator_image

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        tty = True
        self._logging_client.log_tty(tty)
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        # TODO: Not sure if emulator-proxy needs to have access to CAN Network
        networks = self._config_model.required_networks
        self._logging_client.log_networks(networks)
        return networks

    def generate_healthcheck(self) -> Optional[IntermediateHealthcheck]:
        """Check to see if emulator proxy service has started it's python service."""
        return None

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        return None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        return self._monorepo_source.generate_emulator_mount_strings()

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        ports = None
        self._logging_client.log_ports(ports)
        return ports

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        env_vars = {}
        for module in self.MODULE_TYPES:
            proxy_info_items = module.get_proxy_info_env_var().items()  # type: ignore [attr-defined]
            for env_var_name, env_var_value in proxy_info_items:
                env_vars[env_var_name] = env_var_value

        if self._config_model.robot is not None:
            assert issubclass(self._config_model.robot.__class__, RobotInputModel)
            if self._config_model.robot.emulator_proxy_env_vars is not None:
                env_vars.update(self._config_model.robot.emulator_proxy_env_vars)

        self._logging_client.log_env_vars(env_vars)
        return env_vars
