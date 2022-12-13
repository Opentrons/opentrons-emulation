"""Module containing ConcreteOT3ServiceBuilder class."""
from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
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
from emulation_system.consts import OT3_STATE_MANAGER_BOUND_PORT

from ...images import (
    OT3BootloaderImage,
    OT3GantryXImage,
    OT3GantryYImage,
    OT3GripperImage,
    OT3HeadImage,
    OT3PipettesImage,
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
        self._logging_client = OT3LoggingClient(service_info.ot3_hardware, self._dev)
        self._ot3_image = self._generate_image()

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        image_name = self._service_info.image.image_name
        return image_name

    def __get_custom_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        image = self._service_info.image
        env_vars: IntermediateEnvironmentVariables | None = None
        assert isinstance(self._config_model.robot, OT3InputModel)
        match image:
            case OT3PipettesImage():
                env_vars = self._config_model.robot.pipettes_env_vars
            case OT3GripperImage():
                env_vars = self._config_model.robot.gripper_env_vars
            case OT3HeadImage():
                env_vars = self._config_model.robot.head_env_vars
            case OT3GantryXImage():
                env_vars = self._config_model.robot.gantry_x_env_vars
            case OT3GantryYImage():
                env_vars = self._config_model.robot.gantry_y_env_vars
            case OT3BootloaderImage():
                env_vars = self._config_model.robot.bootloader_env_vars
        return env_vars

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self._service_info.ot3_hardware, system_unique_id
        )
        self._logging_client.log_container_name(
            self._service_info.ot3_hardware, container_name, system_unique_id
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

    def generate_healthcheck(self) -> Optional[IntermediateHealthcheck]:
        """Check to see if OT-3 service has established connection to CAN Service."""
        return None

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        return None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        volumes: IntermediateVolumes = [
            self.ENTRYPOINT_MOUNT_STRING,
            self._service_info.ot3_hardware.generate_emulator_volume_string(),
            "state_manager_venv:/ot3-firmware/build-host/.venv",
        ]

        self._logging_client.log_volumes(volumes)
        return volumes

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
            "CAN_SERVER_HOST": self._can_server_service_name,
        }
        if not isinstance(self._service_info.image, OT3BootloaderImage):
            env_vars["STATE_MANAGER_HOST"] = self._state_manager_name
            env_vars["STATE_MANAGER_PORT"] = OT3_STATE_MANAGER_BOUND_PORT

        if isinstance(self._service_info.image, (OT3PipettesImage, OT3GripperImage)):
            env_vars["EEPROM_FILENAME"] = "eeprom.bin"

        custom_env_vars = self.__get_custom_env_vars()
        if custom_env_vars is not None:
            env_vars.update(custom_env_vars)

        self._logging_client.log_env_vars(env_vars)
        return env_vars
