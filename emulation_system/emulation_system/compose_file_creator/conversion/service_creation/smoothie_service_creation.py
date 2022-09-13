"""Pure functions related to the creation of the smoothie Service."""

import json
from typing import List, Optional, Union

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.errors import (
    HardwareDoesNotExistError,
    IncorrectHardwareError,
)
from emulation_system.compose_file_creator.images import SmoothieImages
from emulation_system.compose_file_creator.output.compose_file_model import (
    ListOrDict,
    Volume1,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    OpentronsRepository,
    SourceType,
)

from .shared_functions import (
    add_opentrons_named_volumes,
    generate_container_name,
    get_build_args,
    get_entrypoint_mount_string,
    get_service_build,
    get_service_image,
)


def create_smoothie_service(
    config_model: SystemConfigurationModel,
    global_settings: OpentronsEmulationConfiguration,
    dev: bool,
) -> Service:
    """Create smoothie service."""
    ot2 = config_model.robot

    if ot2 is None:
        raise HardwareDoesNotExistError(Hardware.OT2)
    if ot2.hardware != Hardware.OT2:
        raise IncorrectHardwareError(ot2.hardware, Hardware.OT2)

    smoothie_images = SmoothieImages()
    # Because creation of Smoothie Service should be invisible to user, we want to infer
    # source type of smoothie from source type specified in robot.
    image = (
        smoothie_images.local_firmware_image_name
        if ot2.source_type == SourceType.LOCAL
        else smoothie_images.remote_firmware_image_name
    )

    smoothie_name = generate_container_name("smoothie", config_model)
    # Pulling pipettes from robot because they are actually defined on smoothie, not
    # robot server.
    env = ot2.hardware_specific_attributes.dict()
    env["port"] = 11000
    converted_env = ListOrDict(__root__={"OT_EMULATOR_smoothie": json.dumps(env)})
    repo = OpentronsRepository.OPENTRONS
    build_args = (
        get_build_args(
            repo,
            ot2.source_location,
            global_settings.get_repo_commit(repo),
            global_settings.get_repo_head(repo),
        )
        if ot2.source_type == SourceType.REMOTE
        else None
    )
    mounts: Optional[List[Union[str, Volume1]]] = None
    if ot2.source_type == SourceType.LOCAL:
        mounts = [get_entrypoint_mount_string()]
        mounts.extend(ot2.get_mount_strings())
        add_opentrons_named_volumes(mounts)

    return Service(
        container_name=smoothie_name,
        image=get_service_image(image),
        build=get_service_build(image, build_args, dev),
        networks=config_model.required_networks,
        volumes=mounts,
        tty=True,
        environment=converted_env,
    )
