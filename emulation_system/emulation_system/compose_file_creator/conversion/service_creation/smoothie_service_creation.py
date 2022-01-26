"""Pure functions related to the creation of the smoothie Service."""

import json

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    RequiredNetworks,
)
from .shared_functions import (
    generate_container_name,
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
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import SmoothieImages


def create_smoothie_service(
    config_model: SystemConfigurationModel, required_networks: RequiredNetworks
) -> Service:
    """Create smoothie service."""
    ot2 = config_model.robot
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

    return Service(
        container_name=smoothie_name,
        image=get_service_image(image),
        build=get_service_build(image),
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
        ports=None
    )
