"""Class for creating intermediate type DockerServices."""
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    cast,
)

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    DockerServices,
    RequiredNetworks,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    RobotInputModel,
    ModuleInputModel,
    OT3InputModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    ListOrDict,
    Port,
    Service,
    Volume1,
)
from emulation_system.compose_file_creator.settings.custom_types import Containers
from emulation_system.compose_file_creator.settings.images import EmulatorProxyImages
from emulation_system.consts import DOCKERFILE_DIR_LOCATION


def _generate_container_name(
    container_id: str, config_model: SystemConfigurationModel
) -> str:
    return (
        f"{config_model.system_unique_id}-{container_id}"
        if config_model.system_unique_id is not None
        else container_id
    )


def _get_service_depends_on(
    container: Containers, emulator_proxy_name: Optional[str]
) -> Optional[List[str]]:
    return (
        [emulator_proxy_name]
        if emulator_proxy_name is not None
        and issubclass(container.__class__, ModuleInputModel)
        else None
    )


def _get_command(
    container: Containers, emulator_proxy_name: Optional[str]
) -> Optional[str]:
    depends_on = _get_service_depends_on(container, emulator_proxy_name)
    return depends_on[0] if depends_on is not None else None


def _get_port_bindings(
    container: Containers,
) -> Optional[List[Union[float, str, Port]]]:
    port_bindings = []

    if issubclass(container.__class__, RobotInputModel):
        port_bindings.append(container.get_port_binding_string())

    return cast(Optional[List[Union[float, str, Port]]], port_bindings)


def _get_env_vars(
    container: Containers, emulator_proxy_name: Optional[str]
) -> ListOrDict:
    temp_vars: Dict[str, Any] = {}

    if emulator_proxy_name is not None and issubclass(
        container.__class__, RobotInputModel
    ):
        # TODO: If emulator proxy port is ever not hardcoded will have to update from
        #  11000 to a variable
        temp_vars["OT_SMOOTHIE_EMULATOR_URI"] = f"socket://{emulator_proxy_name}:11000"
        temp_vars["OT_EMULATOR_module_server"] = f'{{"host": "{emulator_proxy_name}"}}'
    elif issubclass(container.__class__, OT3InputModel):
        temp_vars["OT_API_FF_enableOT3HardwareController"] = True
    else:
        temp_vars = {}

    return cast(ListOrDict, temp_vars)


def _get_service_image(container: Containers) -> str:
    return f"{container.get_image_name()}:latest"


def _get_service_build(container: Containers) -> BuildItem:
    return BuildItem(context=DOCKERFILE_DIR_LOCATION, target=container.get_image_name())


def _get_mount_strings(container: Containers) -> Optional[List[Union[str, Volume1]]]:
    mount_strings = container.get_mount_strings()
    return (
        cast(List[Union[str, Volume1]], mount_strings)
        if len(mount_strings) > 0
        else None
    )


def _configure_service(
    container: Containers,
    emulator_proxy_name: Optional[str],
    config_model: SystemConfigurationModel,
    required_networks: RequiredNetworks,
) -> Service:
    service = Service(
        container_name=_generate_container_name(container.id, config_model),
        image=_get_service_image(container),
        tty=True,
        build=_get_service_build(container),
        networks=required_networks.networks,
        volumes=_get_mount_strings(container),
        depends_on=_get_service_depends_on(container, emulator_proxy_name),
        ports=_get_port_bindings(container),
        command=_get_command(container, emulator_proxy_name),
        environment=_get_env_vars(container, emulator_proxy_name),
    )
    return service


def create_services(
    config_model: SystemConfigurationModel, required_networks: RequiredNetworks
) -> DockerServices:
    """Creates all services to be added to compose file."""
    services = {}
    emulator_proxy_name = None

    if config_model.modules_exist:
        # Going to just use the remote image for now. If someone ends up needing
        # the local image it can get added later.
        image = EmulatorProxyImages().remote_firmware_image_name
        emulator_proxy_name = _generate_container_name("emulator-proxy", config_model)
        services[emulator_proxy_name] = Service(
            container_name=emulator_proxy_name,
            image=f"{image}:latest",
            build=BuildItem(context=DOCKERFILE_DIR_LOCATION, target=image),
            tty=True,
            networks=required_networks.networks,
        )

    services.update(
        {
            _generate_container_name(container.id, config_model): _configure_service(
                container, emulator_proxy_name, config_model, required_networks
            )
            for container in config_model.containers.values()
        }
    )

    return DockerServices(services)
