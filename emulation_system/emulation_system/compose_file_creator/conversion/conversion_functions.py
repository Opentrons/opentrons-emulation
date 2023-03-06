"""Functions for converting from SystemConfigurationModel to RuntimeComposeFileModel."""
from typing import Any, Dict, List, Optional, cast

from pydantic import parse_obj_as

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import Service

from ..output.compose_file_model import Network, Volume
from ..output.runtime_compose_file_model import RuntimeComposeFileModel
from . import ServiceOrchestrator


def _get_top_level_volumes(service_list: List[Service]) -> Optional[Dict[str, Volume]]:
    """Get top level volumes dict."""
    mount_list = set()
    for service in service_list:
        if service.volumes is not None:
            mount_list.update(list(service.volumes))
    if len(mount_list) > 0:
        volume_dict = {}
        for mount in mount_list:
            mount = cast(str, mount)
            if not mount.startswith("/"):
                mount_name = mount[: mount.find(":")]
                volume_dict[mount_name] = Volume()
        return volume_dict
    else:
        return None


def _convert(
    config_model: SystemConfigurationModel,
    global_settings: OpentronsEmulationConfiguration,
    dev: bool,
) -> RuntimeComposeFileModel:
    """Parses SystemConfigurationModel to compose file."""
    services = ServiceOrchestrator(config_model, global_settings, dev).build_services()
    return RuntimeComposeFileModel(
        is_remote=config_model.is_remote,
        services=services,
        networks={
            network_name: Network() for network_name in config_model.required_networks
        },
        volumes=_get_top_level_volumes(list(services.values())),
    )


def convert_from_obj(
    input_obj: Dict[str, Any],
    global_settings: OpentronsEmulationConfiguration,
    dev: bool,
) -> RuntimeComposeFileModel:
    """Parse from obj."""
    return _convert(
        parse_obj_as(SystemConfigurationModel, input_obj), global_settings, dev
    )
