"""Logic for creating OT3 emulated hardware services."""
from dataclasses import dataclass
from typing import List

from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from .shared_functions import (
    generate_container_name,
    get_build_args,
    get_mount_strings,
    get_service_build,
)
from ..intermediate_types import RequiredNetworks
from ...errors import (
    HardwareDoesNotExistError,
    IncorrectHardwareError,
)
from ...input.configuration_file import SystemConfigurationModel
from ...output.compose_file_model import Service
from ...settings.config_file_settings import (
    Hardware,
    OT3Hardware,
    OpentronsRepository,
    SourceType,
)
from ...settings.images import (
    Images,
    OT3GantryXImages,
    OT3GantryYImages,
    OT3HeadImages,
    OT3PipettesImages,
)


@dataclass
class ServiceInfo:
    """Info about service to be created."""

    image: Images
    container_name: OT3Hardware


SERVICES_TO_CREATE = [
    ServiceInfo(OT3HeadImages(), OT3Hardware.HEAD),
    ServiceInfo(OT3PipettesImages(), OT3Hardware.PIPETTES),
    ServiceInfo(OT3GantryXImages(), OT3Hardware.GANTRY_X),
    ServiceInfo(OT3GantryYImages(), OT3Hardware.GANTRY_Y),
]


def create_ot3_services(
    config_model: SystemConfigurationModel,
    required_networks: RequiredNetworks,
    global_settings: OpentronsEmulationConfiguration,
) -> List[Service]:
    """Create emulated OT3 hardware services."""
    ot3 = config_model.robot

    if ot3 is None:
        raise HardwareDoesNotExistError(Hardware.OT3)
    if ot3.hardware != Hardware.OT3:
        raise IncorrectHardwareError(ot3.hardware, Hardware.OT3)

    ot3_services = []

    for service_info in SERVICES_TO_CREATE:
        image_name = (
            service_info.image.local_hardware_image_name
            if ot3.source_type == SourceType.LOCAL
            else service_info.image.remote_hardware_image_name
        )
        assert image_name is not None
        container_name = generate_container_name(
            service_info.container_name, config_model
        )
        repo = OpentronsRepository.OT3_FIRMWARE
        build_args = (
            get_build_args(
                repo,
                "latest",
                global_settings.get_repo_commit(repo),
                global_settings.get_repo_head(repo),
            )
            if ot3.source_type == SourceType.REMOTE
            else None
        )
        ot3_services.append(
            Service(
                container_name=container_name,
                image=image_name,
                build=get_service_build(image_name, build_args),
                networks=required_networks.networks,
                volumes=get_mount_strings(ot3),
                tty=True,
            )
        )
    return ot3_services
