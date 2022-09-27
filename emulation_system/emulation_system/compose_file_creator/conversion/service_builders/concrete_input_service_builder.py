"""Module containing ConcreteInputServiceBuilder."""
from typing import Any, Dict, Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    SourceType,
)
from emulation_system.compose_file_creator.conversion.service_creation.shared_functions import (
    get_build_args,
    get_mount_strings,
    get_service_build,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)

from ...input.hardware_models import (
    ModuleInputModel,
    OT2InputModel,
    OT3InputModel,
    RobotInputModel,
)
from ...types.input_types import Containers
from .abstract_service_builder import AbstractServiceBuilder


class ConcreteInputServiceBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building an Input Service."""

    SMOOTHIE_NAME = "smoothie"

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
        container: Containers,
        emulator_proxy_name: Optional[str],
        smoothie_name: Optional[str],
        can_server_service_name: Optional[str],
    ) -> None:
        """Instantiates a ConcreteInputServiceBuilder object."""
        super().__init__(config_model, global_settings)
        self._container = container
        self._emulator_proxy_name = emulator_proxy_name
        self._smoothie_name = smoothie_name
        self._can_server_service_name = can_server_service_name
        self._dev = dev
        self._image = self._generate_image()

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        return self._container.get_image_name()

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self._container.id, system_unique_id
        )
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return f"{self._image}:latest"

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        tty = True
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        networks = self._config_model.required_networks
        return networks

    def generate_build(self) -> Optional[BuildItem]:
        """Generates value for build parameter."""
        build_args = None
        source_location = None
        if (
            issubclass(self._container.__class__, RobotInputModel)
            and self._container.robot_server_source_type == SourceType.REMOTE
        ):
            source_location = self._container.robot_server_source_location
        elif (
            not issubclass(self._container.__class__, RobotInputModel)
            and self._container.source_type == SourceType.REMOTE
        ):
            source_location = self._container.source_location

        if source_location is not None:
            repo = self._container.get_source_repo()
            build_args = get_build_args(
                repo,
                source_location,
                self._global_settings.get_repo_commit(repo),
                self._global_settings.get_repo_head(repo),
            )
        return get_service_build(self._image, build_args, self._dev)

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        return get_mount_strings(self._container)

    def generate_command(self) -> Optional[IntermediateCommand]:
        """Generates value for command parameter."""
        command = None
        if self._emulator_proxy_name is not None:
            if self._container.emulation_level == EmulationLevels.HARDWARE:
                command = self._container.get_hardware_level_command(
                    self._emulator_proxy_name
                )
            else:
                command = self._container.get_firmware_level_command(
                    self._emulator_proxy_name
                )

        return command

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        ports = None
        if issubclass(self._container.__class__, RobotInputModel):
            ports = [self._container.get_port_binding_string()]
        return ports

    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        """Generates value for depends_on parameter."""
        dependencies = []
        if self._emulator_proxy_name is not None:
            dependencies.append(self._emulator_proxy_name)

        if self._smoothie_name is not None and issubclass(
            self._container.__class__, OT2InputModel
        ):
            dependencies.append(self._smoothie_name)

        return dependencies if len(dependencies) != 0 else None

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        temp_vars: Dict[str, Any] = {}

        if (
            issubclass(self._container.__class__, RobotInputModel)
            and self._emulator_proxy_name is not None
        ):
            temp_vars[
                "OT_EMULATOR_module_server"
            ] = f'{{"host": "{self._emulator_proxy_name}"}}'

        if issubclass(self._container.__class__, OT2InputModel):
            # TODO: If emulator proxy port is ever not hardcoded will have to update from
            #  11000 to a variable
            temp_vars[
                "OT_SMOOTHIE_EMULATOR_URI"
            ] = f"socket://{self._smoothie_name}:11000"

        if issubclass(self._container.__class__, OT3InputModel):
            temp_vars["OT_API_FF_enableOT3HardwareController"] = True
            temp_vars["OT3_CAN_DRIVER_interface"] = "opentrons_sock"
            temp_vars["OT3_CAN_DRIVER_host"] = self._can_server_service_name
            temp_vars["OT3_CAN_DRIVER_port"] = 9898

        if issubclass(self._container.__class__, ModuleInputModel):
            temp_vars.update(self._container.get_serial_number_env_var())
            temp_vars.update(self._container.get_proxy_info_env_var())
        return temp_vars
