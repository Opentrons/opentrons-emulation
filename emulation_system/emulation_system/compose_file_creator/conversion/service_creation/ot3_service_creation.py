"""Logic for creating OT3 emulated hardware services."""
from dataclasses import dataclass
from typing import List, Optional, cast

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.config_file_settings import (
    Hardware,
    OpentronsRepository,
    OT3Hardware,
    SourceType,
)
from emulation_system.compose_file_creator.images import (
    Images,
    OT3BootloaderImages,
    OT3GantryXImages,
    OT3GantryYImages,
    OT3GripperImages,
    OT3HeadImages,
    OT3PipettesImages,
)

from ...errors import HardwareDoesNotExistError, IncorrectHardwareError
from ...input.configuration_file import SystemConfigurationModel
from ...output.compose_file_model import ListOrDict
from ...types.final_types import ServiceVolumes
from .shared_functions import (
    add_ot3_firmware_named_volumes,
    generate_container_name,
    get_build_args,
    get_entrypoint_mount_string,
    get_service_build,
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
    ServiceInfo(OT3BootloaderImages(), OT3Hardware.BOOTLOADER),
    ServiceInfo(OT3GripperImages(), OT3Hardware.GRIPPER),
]


def create_ot3_services(
    config_model: SystemConfigurationModel,
    global_settings: OpentronsEmulationConfiguration,
    can_server_name: str,
    dev: bool,
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
                ot3.source_location,
                global_settings.get_repo_commit(repo),
                global_settings.get_repo_head(repo),
            )
            if ot3.source_type == SourceType.REMOTE
            else None
        )

        mounts: Optional[List[str]] = None
        if ot3.source_type == SourceType.LOCAL:
            mounts = [get_entrypoint_mount_string()]
            mounts.extend(ot3.get_mount_strings())
            add_ot3_firmware_named_volumes(mounts)
        env = ListOrDict(__root__={"CAN_SERVER_HOST": can_server_name})
        ot3_services.append(
            Service(
                container_name=container_name,
                image=image_name,
                build=get_service_build(image_name, build_args, dev),
                networks=config_model.required_networks,
                volumes=cast(ServiceVolumes, mounts),
                tty=True,
                environment=env,
            )
        )
    return ot3_services
