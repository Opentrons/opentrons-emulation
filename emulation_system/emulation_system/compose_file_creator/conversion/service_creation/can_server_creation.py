"""Pure functions related to creating emulator-proxy service."""
from typing import (
    List,
    Optional,
    Union,
)

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    RequiredNetworks,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    ListOrDict,
    Service,
    Volume1,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import CANServerImages
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from .shared_functions import (
    generate_container_name,
    get_build_args,
    get_entrypoint_mount_string,
    get_service_build,
    get_service_image,
)
from ...errors import (
    HardwareDoesNotExistError,
    IncorrectHardwareError,
)

MODULE_TYPES = [
    ThermocyclerModuleInputModel,
    TemperatureModuleInputModel,
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
]


def _create_emulator_proxy_env_vars() -> ListOrDict:
    # Build dict of all module env vars and add them to emulator proxy.
    return ListOrDict(
        __root__={
            env_var_name: env_var_value
            for module in MODULE_TYPES
            for env_var_name, env_var_value in module.get_proxy_info_env_var().items()
            # type: ignore [attr-defined] # noqa: E501
        }
    )


def create_can_server_service(
    config_model: SystemConfigurationModel,
    required_networks: RequiredNetworks,
    global_settings: OpentronsEmulationConfiguration,
) -> Service:
    """Creates emulator-proxy service."""
    # Going to just use the remote image for now. If someone ends up needing
    # the local image it can get added later.
    ot3 = config_model.robot

    if ot3 is None:
        raise HardwareDoesNotExistError(Hardware.OT3)
    if ot3.hardware != Hardware.OT3:
        raise IncorrectHardwareError(ot3.hardware, Hardware.OT3)

    can_server_images = CANServerImages()

    if ot3.can_server_source_type == SourceType.LOCAL:
        image = can_server_images.local_firmware_image_name
    else:
        image = can_server_images.remote_firmware_image_name

    can_server_name = generate_container_name("can-server", config_model)
    repo = OpentronsRepository.OPENTRONS

    mounts: Optional[List[Union[str, Volume1]]] = None
    if ot3.can_server_source_type == SourceType.LOCAL:
        mounts = [get_entrypoint_mount_string()]
        mounts.extend(ot3.get_can_mount_strings())

    build_args = (
        get_build_args(
                repo,
                "latest",
                global_settings.get_repo_commit(repo),
                global_settings.get_repo_head(repo),
        )
        if ot3.can_server_source_type == SourceType.REMOTE
        else None
    )

    return Service(
        container_name=can_server_name,
        image=get_service_image(image),
        build=get_service_build(image, build_args),
        tty=True,
        networks=required_networks.networks,
        volumes=mounts,
    )
