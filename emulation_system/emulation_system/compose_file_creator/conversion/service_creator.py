"""Class for creating intermediate type DockerServices."""
from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.types.intermediate_types import (
    DockerServices,
)

from . import ServiceBuilderOrchestrator


def create_services(
    config_model: SystemConfigurationModel,
    global_settings: OpentronsEmulationConfiguration,
    dev: bool,
) -> DockerServices:
    """Creates all services to be added to compose file."""
    service_builder_orchestrator = ServiceBuilderOrchestrator(
        config_model, global_settings, dev
    )
    services = {}
    smoothie_name = None
    can_server_service_name = None

    emulator_proxy_service = service_builder_orchestrator.build_emulator_proxy_service()
    emulator_proxy_name = emulator_proxy_service.container_name
    assert emulator_proxy_name is not None  # For mypy
    services[emulator_proxy_name] = emulator_proxy_service

    if config_model.has_ot2:
        smoothie_service = service_builder_orchestrator.build_smoothie_service()
        smoothie_name = smoothie_service.container_name
        assert smoothie_name is not None
        services[smoothie_name] = smoothie_service

    if config_model.has_ot3:
        can_server_service = service_builder_orchestrator.build_can_server_service()
        can_server_service_name = can_server_service.container_name
        assert can_server_service_name is not None
        ot3_services = service_builder_orchestrator.build_ot3_services(
            can_server_service_name,
        )
        services[can_server_service_name] = can_server_service
        for ot3_service in ot3_services:
            assert ot3_service.container_name is not None
            services[ot3_service.container_name] = ot3_service

    input_services = service_builder_orchestrator.build_input_services(
        emulator_proxy_name, smoothie_name, can_server_service_name
    )
    for service in input_services:
        assert service.container_name is not None
        services[service.container_name] = service

    return DockerServices(services)
