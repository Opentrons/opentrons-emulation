"""Class for creating intermediate type DockerServices."""
from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.types.intermediate_types import (
    DockerServices,
)

from ..input.hardware_models import OT2InputModel, OT3InputModel
from . import ServiceBuilderOrchestrator
from .service_creation.input_service_creation import configure_input_service
from .service_creation.ot3_service_creation import create_ot3_services
from .service_creation.shared_functions import generate_container_name
from .service_creation.smoothie_service_creation import create_smoothie_service


def create_services(
    config_model: SystemConfigurationModel,
    global_settings: OpentronsEmulationConfiguration,
    dev: bool,
) -> DockerServices:
    """Creates all services to be added to compose file."""
    service_builder_orchestrator = ServiceBuilderOrchestrator(
        config_model, global_settings
    )
    services = {}
    smoothie_name = None
    can_server_service_name = None

    emulator_proxy_service = service_builder_orchestrator.build_emulator_proxy_service(
        dev
    )
    emulator_proxy_name = emulator_proxy_service.container_name
    assert emulator_proxy_name is not None  # For mypy
    services[emulator_proxy_name] = emulator_proxy_service

    if config_model.robot is not None and config_model.robot.__class__ == OT2InputModel:
        smoothie_service = create_smoothie_service(config_model, global_settings, dev)
        smoothie_name = smoothie_service.container_name
        assert smoothie_name is not None
        services[smoothie_name] = smoothie_service

    if config_model.robot is not None and config_model.robot.__class__ == OT3InputModel:
        can_server_service = service_builder_orchestrator.build_can_server_service(dev)
        can_server_service_name = can_server_service.container_name
        assert can_server_service_name is not None
        ot3_services = create_ot3_services(
            config_model,
            global_settings,
            can_server_service_name,
            dev,
        )
        services[can_server_service_name] = can_server_service
        for ot3_service in ot3_services:
            assert ot3_service.container_name is not None
            services[ot3_service.container_name] = ot3_service

    services.update(
        {
            generate_container_name(
                container.id, config_model
            ): configure_input_service(
                container,
                emulator_proxy_name,
                smoothie_name,
                can_server_service_name,
                config_model,
                global_settings,
                dev,
            )
            for container in config_model.containers.values()
        }
    )

    return DockerServices(services)
