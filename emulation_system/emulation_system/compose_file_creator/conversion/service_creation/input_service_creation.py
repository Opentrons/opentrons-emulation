"""Pure functions related to creating Service objects from definitions in input file."""

from typing import Any, Dict, List, Optional, Union

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    RequiredNetworks,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    ModuleInputModel,
    OT2InputModel,
    OT3InputModel,
    RobotInputModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    ListOrDict,
    Port,
    Service,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    SourceType,
)
from emulation_system.compose_file_creator.settings.custom_types import Containers
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


def _get_service_depends_on(
    container: Containers,
    emulator_proxy_name: Optional[str],
    smoothie_name: Optional[str],
) -> Optional[List[str]]:
    dependencies = []
    if emulator_proxy_name is not None:
        dependencies.append(emulator_proxy_name)

    if smoothie_name is not None and issubclass(container.__class__, OT2InputModel):
        dependencies.append(smoothie_name)

    return dependencies if len(dependencies) != 0 else None


def _get_command(
    container: Containers, emulator_proxy_name: Optional[str]
) -> Optional[List[str]]:
    # If emulator proxy exists and container is module then the emulator proxy name
    # should be the command.
    command: Optional[List[str]] = None
    if emulator_proxy_name is not None:
        if container.emulation_level == EmulationLevels.HARDWARE:
            command = container.get_hardware_level_command(emulator_proxy_name)
        else:
            command = container.get_firmware_level_command(emulator_proxy_name)

    return command


def _get_port_bindings(
    container: Containers,
) -> Optional[List[Union[float, str, Port]]]:
    # If container is a robot add a port binding.
    if issubclass(container.__class__, RobotInputModel):
        return [container.get_port_binding_string()]
    else:
        return None


def _get_env_vars(
    container: Containers,
    emulator_proxy_name: Optional[str],
    smoothie_name: Optional[str],
    can_server_service_name: Optional[str],
) -> ListOrDict:
    temp_vars: Dict[str, Any] = {}

    if (
        issubclass(container.__class__, RobotInputModel)
        and emulator_proxy_name is not None
    ):
        temp_vars["OT_EMULATOR_module_server"] = f'{{"host": "{emulator_proxy_name}"}}'

    if issubclass(container.__class__, OT2InputModel):
        # TODO: If emulator proxy port is ever not hardcoded will have to update from
        #  11000 to a variable
        temp_vars["OT_SMOOTHIE_EMULATOR_URI"] = f"socket://{smoothie_name}:11000"

    if issubclass(container.__class__, OT3InputModel):
        temp_vars["OT_API_FF_enableOT3HardwareController"] = True
        temp_vars["OT3_CAN_DRIVER_interface"] = "opentrons_sock"
        temp_vars["OT3_CAN_DRIVER_host"] = can_server_service_name
        temp_vars["OT3_CAN_DRIVER_port"] = 9898

    if issubclass(container.__class__, ModuleInputModel):
        temp_vars.update(container.get_serial_number_env_var())
        temp_vars.update(container.get_proxy_info_env_var())

    return ListOrDict(__root__=temp_vars)


def configure_input_service(
    container: Containers,
    emulator_proxy_name: Optional[str],
    smoothie_name: Optional[str],
    can_server_service_name: Optional[str],
    config_model: SystemConfigurationModel,
    required_networks: RequiredNetworks,
    global_settings: OpentronsEmulationConfiguration,
) -> Service:
    """Configures services that are defined in input file."""
    build_args = None
    source_location = None
    if (
        issubclass(container.__class__, RobotInputModel)
        and container.robot_server_source_type == SourceType.REMOTE
    ):
        source_location = container.robot_server_source_location
    elif (
        not issubclass(container.__class__, RobotInputModel)
        and container.source_type == SourceType.REMOTE
    ):
        source_location = container.source_location

    if source_location is not None:
        repo = container.get_source_repo()
        build_args = get_build_args(
            repo,
            source_location,
            global_settings.get_repo_commit(repo),
            global_settings.get_repo_head(repo),
        )

    service = Service(
        container_name=generate_container_name(container.id, config_model),
        image=get_service_image(container.get_image_name()),
        tty=True,
        build=get_service_build(container.get_image_name(), build_args),
        networks=required_networks.networks,
        volumes=get_mount_strings(container),
        depends_on=_get_service_depends_on(
            container, emulator_proxy_name, smoothie_name
        ),
        ports=_get_port_bindings(container),
        command=_get_command(container, emulator_proxy_name),
        environment=_get_env_vars(
            container, emulator_proxy_name, smoothie_name, can_server_service_name
        ),
    )
    return service
