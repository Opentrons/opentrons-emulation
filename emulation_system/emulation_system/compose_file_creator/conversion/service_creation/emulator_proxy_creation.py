"""Pure functions related to creating emulator-proxy service."""

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
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.compose_file_creator.settings.images import EmulatorProxyImages
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)

from .shared_functions import (
    generate_container_name,
    get_build_args,
    get_service_build,
    get_service_image,
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


def create_emulator_proxy_service(
    config_model: SystemConfigurationModel,
    global_settings: OpentronsEmulationConfiguration,
    dev: bool,
) -> Service:
    """Creates emulator-proxy service."""
    # Going to just use the remote image for now. If someone ends up needing
    # the local image it can get added later.
    image = EmulatorProxyImages().remote_firmware_image_name
    emulator_proxy_name = generate_container_name("emulator-proxy", config_model)
    repo = OpentronsRepository.OPENTRONS
    return Service(
        container_name=emulator_proxy_name,
        image=get_service_image(image),
        build=get_service_build(
            image_name=image,
            # Will always have build args since we are always using the remote image
            build_args=get_build_args(
                repo,
                "latest",
                global_settings.get_repo_commit(repo),
                global_settings.get_repo_head(repo),
            ),
            dev=dev,
        ),
        tty=True,
        networks=config_model.required_networks,
        environment=_create_emulator_proxy_env_vars(),
    )
