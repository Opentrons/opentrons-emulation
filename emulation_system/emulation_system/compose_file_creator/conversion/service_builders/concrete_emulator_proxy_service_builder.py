"""Module containing ConcreteEmulatorProxyServiceBuilder class."""

from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.compose_file_creator.conversion.service_creation.shared_functions import (
    get_build_args,
    get_service_build,
    get_service_image,
)
from emulation_system.compose_file_creator.images import EmulatorProxyImages
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)

from ...logging import EmulatorProxyLoggingClient
from .abstract_service_builder import AbstractServiceBuilder


class ConcreteEmulatorProxyServiceBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building an Emulator Proxy."""

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
        """Instantiates a ConcreteEmulatorProxyServiceBuilder object."""
        super().__init__(config_model, global_settings)
        self._dev = dev
        self._logging_client = EmulatorProxyLoggingClient(self._dev)
        self._image = self._generate_image()

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        image_name = EmulatorProxyImages().remote_firmware_image_name
        # Passing blank strings because EmulatorProxyLoggingClient overrides
        # LoggingClient's log_image_name method, but doesn't need the last 2 parameters.
        # But those parameters need to be there to match the parent's signature.
        self._logging_client.log_image_name(image_name, "", "")
        return image_name

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
        return get_service_image(self._image)

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

    def generate_build(self) -> Optional[BuildItem]:
        """Generates value for build parameter."""
        repo = OpentronsRepository.OPENTRONS
        build_args = get_build_args(
            repo,
            "latest",
            self._global_settings.get_repo_commit(repo),
            self._global_settings.get_repo_head(repo),
        )
        self._logging_client.log_build_args(build_args)
        return get_service_build(self._image, build_args, self._dev)

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
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
        ports = None
        self._logging_client.log_ports(ports)
        return ports

    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        """Generates value for depends_on parameter."""
        depends_on = None
        self._logging_client.log_depends_on(depends_on)
        return depends_on

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        env_vars = {
            env_var_name: env_var_value
            for module in self.MODULE_TYPES
            for env_var_name, env_var_value in module.get_proxy_info_env_var().items()  # type: ignore [attr-defined]
        }
        self._logging_client.log_env_vars(env_vars)
        return env_vars
