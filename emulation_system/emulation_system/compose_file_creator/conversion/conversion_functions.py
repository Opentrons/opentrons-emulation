"""Functions for converting from SystemConfigurationModel to RuntimeComposeFileModel."""
import os

from typing import (
    Any,
    Dict,
    cast,
)

from pydantic import (
    parse_file_as,
    parse_obj_as,
)

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    RequiredNetworks,
)
from emulation_system.compose_file_creator.conversion.service_creator import (
    create_services,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    Network,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DEFAULT_NETWORK_NAME,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)


class FileDisambiguationError(Exception):
    """Exception thrown when there is multiple files with specified relative path."""

    ...


def _get_required_networks(
    config_model: SystemConfigurationModel,
) -> RequiredNetworks:
    """Get required networks to create for system."""
    local_network_name = (
        DEFAULT_NETWORK_NAME
        if config_model.system_unique_id is None
        else config_model.system_unique_id
    )

    required_networks = [cast(str, local_network_name)]
    if config_model.requires_can_network:
        required_networks.append(config_model.can_network_name)

    return RequiredNetworks(required_networks)


def _convert(config_model: SystemConfigurationModel) -> RuntimeComposeFileModel:
    """Parses SystemConfigurationModel to compose file."""
    required_networks = _get_required_networks(config_model)
    services = create_services(config_model, required_networks)
    return RuntimeComposeFileModel(
        version=config_model.compose_file_version,
        services=services.services,
        networks={
            network_name: Network() for network_name in required_networks.networks
        },
    )


def convert_from_file(
    settings: OpentronsEmulationConfiguration, input_file_path: str
) -> RuntimeComposeFileModel:
    """Parse from file.

    Will load either an absolute path, or a relative path against paths specified in
    emulation_configuration_file_locations setting.
    """
    if not os.path.isabs(input_file_path):
        extra_locations = (
            settings.global_settings.emulation_configuration_file_locations
        )
        results = []
        for extra_location in extra_locations:
            possible_path = os.path.join(extra_location, input_file_path)
            if os.path.isfile(possible_path):
                results.append(possible_path)

        if len(results) == 0:
            raise FileNotFoundError(
                f"File {input_file_path} not found in any specified"
                f" emulation_configuration_file_locations"
            )
        elif len(results) > 1:
            paths = ", ".join(extra_locations)
            raise FileDisambiguationError(
                f"Specified file found in multiple locations:" f" {paths}"
            )
        else:
            input_file_path = results[0]

    return _convert(parse_file_as(SystemConfigurationModel, input_file_path))


def convert_from_obj(input_obj: Dict[str, Any]) -> RuntimeComposeFileModel:
    """Parse from obj."""
    return _convert(parse_obj_as(SystemConfigurationModel, input_obj))
