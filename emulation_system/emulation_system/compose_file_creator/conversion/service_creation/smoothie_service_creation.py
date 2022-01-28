"""Pure functions related to the creation of the smoothie Service."""

import json

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    RequiredNetworks,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from .shared_functions import (
    generate_container_name,
    get_build_args,
    get_mount_strings,
    get_service_build,
    get_service_image,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    ListOrDict,
    Service,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import SmoothieImages
from ...errors import (
    HardwareDoesNotExistError,
    IncorrectHardwareError,
)


def create_smoothie_service(
    config_model: SystemConfigurationModel,
    required_networks: RequiredNetworks,
    global_settings: OpentronsEmulationConfiguration,
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
    converted_env = ListOrDict(
        __root__={
            "OT_EMULATOR_smoothie": json.dumps(ot2.hardware_specific_attributes.dict())
        }
    )
    build_args = (
        get_build_args(OpentronsRepository.OPENTRONS, "latest", global_settings)
        if ot2.source_type == SourceType.REMOTE
        else None
    )

    return Service(
        container_name=smoothie_name,
        image=get_service_image(image),
        build=get_service_build(image, build_args),
        networks=required_networks.networks,
        # Using ot2 mount strings here. This will add the constraint that robot-server
        # and smoothie use same source code. Going to leave this for now until it
        # becomes a problem.
        volumes=get_mount_strings(ot2),
        tty=True,
        environment=converted_env,
        # Intentionally not specifying command. Smoothie uses a separate executable
        # from the other firmware emulations. This executable is hardcoded to be run
        # when running a smoothie type container. See run-smoothie inside entrypoint.sh
        command=None,
        # No ports needed for smoothie
        ports=None,
    )
