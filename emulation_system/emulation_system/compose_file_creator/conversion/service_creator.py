"""Class for creating intermediate type DockerServices."""
from typing import (
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
    """Generates container name based off of system_unique_id value."""
    return (
        f"{config_model.system_unique_id}-{container_id}"
        if config_model.system_unique_id is not None
        else container_id
    )


def _get_service_depends_on(
    emulator_proxy_name: Optional[str], container: Containers
) -> Optional[List[str]]:
    """Get list of other services that service depends on.

    If service is module, return [emulator_proxy_name]
    """
    return (
        [emulator_proxy_name]
        if emulator_proxy_name is not None
        and container.is_module()
        else None
    )


def _get_command(
    emulator_proxy_name: Optional[str], container: Containers
) -> Optional[str]:
    """Get command for service to run.

    If service is module, return emulator_proxy_name
    """
    depends_on = _get_service_depends_on(emulator_proxy_name, container)
    return depends_on[0] if depends_on is not None else None


def _get_port_bindings(
    container: Containers,
) -> Optional[List[Union[float, str, Port]]]:
    port_string = (
        [container.get_port_binding_string()]
        if container.is_robot()
        else None
    )
    return cast(Optional[List[Union[float, str, Port]]], port_string)


def _generate_robot_server_env_vars(
    emulator_proxy_name: str, emulator_proxy_port: int
) -> Dict[str, str]:
    return {
        "OT_SMOOTHIE_EMULATOR_URI": f"socket://{emulator_proxy_name}:"
        f"{emulator_proxy_port}",
        "OT_EMULATOR_module_server": f'{{"host": "{emulator_proxy_name}"}}',
    }


def _configure_service(
    container: Containers,
    emulator_proxy_name: Optional[str],
    config_model: SystemConfigurationModel,
    required_networks: RequiredNetworks,
) -> Service:
    """Configure and return an individual service."""
    service_image = f"{container.get_image_name()}:latest"
    service_build = BuildItem(
        context=DOCKERFILE_DIR_LOCATION, target=container.get_image_name()
    )
    mount_strings = cast(List[Union[str, Volume1]], container.get_mount_strings())

    if emulator_proxy_name is not None and container.is_robot():
        # To get mypy to realize that emulator_proxy_name can't be None here
        assert emulator_proxy_name is not None
        temp_vars = _generate_robot_server_env_vars(emulator_proxy_name, 11000)
    else:
        temp_vars = {}

    env_vars = cast(ListOrDict, temp_vars)

    service = Service(
        container_name=_generate_container_name(container.id, config_model),
        image=service_image,
        tty=True,
        build=service_build,
        networks=required_networks.networks,
        volumes=mount_strings if len(mount_strings) > 0 else None,
        depends_on=_get_service_depends_on(emulator_proxy_name, container),
        ports=_get_port_bindings(container),
        command=_get_command(emulator_proxy_name, container),
        environment=env_vars,
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
