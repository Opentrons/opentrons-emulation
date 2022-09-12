from emulation_system.compose_file_creator.conversion.builders.service_builders.concrete_can_server_service_builder import (
    ConcreteCANServerServiceBuilder,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import Service
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
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
