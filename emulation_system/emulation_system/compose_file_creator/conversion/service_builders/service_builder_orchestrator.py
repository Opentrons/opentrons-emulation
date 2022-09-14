"""Module containing ServiceBuilderOrchestrator class."""

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.conversion import (
    ConcreteCANServerServiceBuilder,
    ConcreteEmulatorProxyServiceBuilder,
)


class ServiceBuilderOrchestrator:
    """Class that client uses to interface with builders."""

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
    ) -> None:
        """Instantiates a ServiceBuilderOrchestrator object."""
        self._config_model = config_model
        self._global_settings = global_settings

    def build_can_server_service(self, dev: bool) -> Service:
        """Method to generate and return a CAN Server Service."""
        return ConcreteCANServerServiceBuilder(
            self._config_model, self._global_settings, dev
        ).build_service()

    def build_emulator_proxy_service(self, dev: bool) -> Service:
        """Method to generate and return an Emulator Proxy Service."""
        return ConcreteEmulatorProxyServiceBuilder(
            self._config_model, self._global_settings, dev
        ).build_service()
