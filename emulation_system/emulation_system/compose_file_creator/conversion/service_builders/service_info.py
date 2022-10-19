"""ServiceInfo Class."""

from dataclasses import dataclass

from emulation_system.compose_file_creator.config_file_settings import OT3Hardware
from emulation_system.compose_file_creator.images import Images


@dataclass
class ServiceInfo:
    """Info about service to be created."""

    image: Images
    container_name: OT3Hardware
