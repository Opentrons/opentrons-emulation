from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.conversion import (
    ConcreteCANServerServiceBuilder,
)


class ServiceBuilderOrchestrator:
    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
    ) -> None:
        self._config_model = config_model
        self._global_settings = global_settings

    def build_can_server_service(self, dev: bool) -> Service:
        service = ConcreteCANServerServiceBuilder(
            self._config_model, self._global_settings, dev
        ).build_service()
        return service
