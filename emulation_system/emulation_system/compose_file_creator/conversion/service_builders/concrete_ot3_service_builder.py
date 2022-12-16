"""Module containing ConcreteOT3ServiceBuilder class."""
from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.compose_file_creator.utilities.shared_functions import (
    add_opentrons_named_volumes,
    add_ot3_firmware_named_volumes,
    get_build_args,
)
from emulation_system.consts import OT3_STATE_MANAGER_BOUND_PORT

from ...images import (
    OT3BootloaderImages,
    OT3GantryXImages,
    OT3GantryYImages,
    OT3GripperImages,
    OT3HeadImages,
    OT3PipettesImages,
)
from ...input.hardware_models import OT3InputModel
from ...logging import OT3LoggingClient
from .abstract_service_builder import AbstractServiceBuilder
from .service_info import ServiceInfo


class ConcreteOT3ServiceBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building OT-3 firmware services."""

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
        can_server_service_name: str,
        state_manager_name: str,
        service_info: ServiceInfo,
    ) -> None:
        """Instantiates a ConcreteOT3ServiceBuilder object."""
        super().__init__(config_model, global_settings, dev)
        self._can_server_service_name = can_server_service_name
        self._state_manager_name = state_manager_name
        self._service_info = service_info
        self._ot3 = self.get_ot3(config_model)
        self._logging_client = OT3LoggingClient(service_info.container_name, self._dev)
        self._ot3_image = self._generate_image()

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        source_type = self._ot3.source_type
        image_name = (
            self._service_info.image.local_hardware_image_name
            if source_type == SourceType.LOCAL
            else self._service_info.image.remote_hardware_image_name
        )
        assert image_name is not None
        self._logging_client.log_image_name(image_name, source_type, "source-type")
        return image_name

    def __get_custom_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        image = self._service_info.image
        env_vars: IntermediateEnvironmentVariables | None = None
        assert isinstance(self._config_model.robot, OT3InputModel)
        match image:
            case OT3PipettesImages():
                env_vars = self._config_model.robot.pipettes_env_vars
            case OT3GripperImages():
                env_vars = self._config_model.robot.gripper_env_vars
            case OT3HeadImages():
                env_vars = self._config_model.robot.head_env_vars
            case OT3GantryXImages():
                env_vars = self._config_model.robot.gantry_x_env_vars
            case OT3GantryYImages():
                env_vars = self._config_model.robot.gantry_y_env_vars
            case OT3BootloaderImages():
                env_vars = self._config_model.robot.bootloader_env_vars
        return env_vars

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self._service_info.container_name, system_unique_id
        )
        self._logging_client.log_container_name(
            self._service_info.container_name, container_name, system_unique_id
        )
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return self._image

    @property
    def _image(self) -> str:
        return self._ot3_image

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        tty = True
        self._logging_client.log_tty(tty)
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        networks = self._config_model.required_networks
        self._logging_client.log_networks(networks)
        return networks

    def generate_healthcheck(self) -> IntermediateHealthcheck:
        """Check to see if OT-3 service has established connection to CAN Service."""
        port = self._ot3.can_server_bound_port
        return IntermediateHealthcheck(
            interval=10,
            retries=6,
            timeout=10,
            command=f"netstat -nputw | grep -E '{port}.*ESTABLISHED'",
        )

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        ot3_firmware_repo = OpentronsRepository.OT3_FIRMWARE
        monorepo = OpentronsRepository.OPENTRONS
        build_args: IntermediateBuildArgs = {}

        if self._ot3.source_type == SourceType.REMOTE:
            ot3_firmware_build_args = get_build_args(
                ot3_firmware_repo,
                self._ot3.source_location,
                self._global_settings.get_repo_branch(ot3_firmware_repo),
                self._global_settings.get_repo_head(ot3_firmware_repo),
            )
            build_args.update(ot3_firmware_build_args)

        if self._ot3.opentrons_hardware_source_type == SourceType.REMOTE:
            monorepo_build_args = get_build_args(
                monorepo,
                self._ot3.opentrons_hardware_source_location,
                self._global_settings.get_repo_branch(monorepo),
                self._global_settings.get_repo_head(monorepo),
            )
            build_args.update(monorepo_build_args)

        args_to_pass = build_args if len(build_args) > 0 else None

        self._logging_client.log_build_args(args_to_pass)
        return args_to_pass

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        volumes: IntermediateVolumes = []
        if SourceType.LOCAL in [
            self._ot3.source_type,
            self._ot3.opentrons_hardware_source_type,
        ]:
            volumes.append(self.ENTRYPOINT_MOUNT_STRING)
            volumes.extend(self._ot3.get_mount_strings())

            if self._ot3.source_type == SourceType.LOCAL:
                add_ot3_firmware_named_volumes(volumes)

            if self._ot3.opentrons_hardware_source_type == SourceType.LOCAL:
                add_opentrons_named_volumes(volumes)

        arg_to_pass = volumes if len(volumes) > 0 else None
        self._logging_client.log_volumes(arg_to_pass)
        return arg_to_pass

    def generate_command(self) -> Optional[IntermediateCommand]:
        """Generates value for command parameter."""
        command = None
        self._logging_client.log_command(command)
        return command

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        ports = None
        self._logging_client.log_ports(ports)
        return ports

    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        """Generates value for depends_on parameter."""
        depends_on = None
        self._logging_client.log_depends_on(depends_on)
        return depends_on

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        env_vars: IntermediateEnvironmentVariables = {
            "CAN_SERVER_HOST": self._can_server_service_name
        }
        if not isinstance(self._service_info.image, OT3BootloaderImages):
            env_vars["STATE_MANAGER_HOST"] = self._state_manager_name
            env_vars["STATE_MANAGER_PORT"] = OT3_STATE_MANAGER_BOUND_PORT

        if isinstance(self._service_info.image, (OT3PipettesImages, OT3GripperImages)):
            env_vars["EEPROM_FILENAME"] = "eeprom.bin"

        custom_env_vars = self.__get_custom_env_vars()
        if custom_env_vars is not None:
            env_vars.update(custom_env_vars)

        self._logging_client.log_env_vars(env_vars)
        return env_vars
