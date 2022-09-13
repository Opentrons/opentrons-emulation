from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.conversion import AbstractServiceBuilder
from emulation_system.compose_file_creator.conversion.service_creation.shared_functions import (
    get_build_args,
    get_service_build,
    get_service_image,
)
from emulation_system.compose_file_creator.images import EmulatorProxyImages
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.intermediate_types import (
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.logging import EmulatorProxyLoggingClient


class ConcreteEmulatorProxyServiceBuilder(AbstractServiceBuilder):

    EMULATOR_PROXY_NAME = "emulator-proxy"

    MODULE_TYPES = [
        ThermocyclerModuleInputModel,
        TemperatureModuleInputModel,
        HeaterShakerModuleInputModel,
        MagneticModuleInputModel,
    ]

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        super().__init__(config_model, global_settings)
        self._dev = dev
        self._logging_client = EmulatorProxyLoggingClient(self._dev)
        self._image = self._generate_image()

    def generate_container_name(self) -> str:
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self.EMULATOR_PROXY_NAME, system_unique_id
        )
        self._logging_client.log_container_name(
            self.EMULATOR_PROXY_NAME, container_name, system_unique_id
        )
        return container_name

    def _generate_image(self) -> str:
        image_name = EmulatorProxyImages().remote_firmware_image_name
        # Passing blank strings because EmulatorProxyLoggingClient overrides
        # LoggingClient's log_image_name method, but doesn't need the last 2 parameters.
        # But those parameters need to be there to match the parent's signature.
        self._logging_client.log_image_name(image_name, "", "")
        return image_name

    def generate_image(self) -> str:
        return get_service_image(self._image)

    def is_tty(self) -> bool:
        tty = True
        self._logging_client.log_tty(tty)
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        # TODO: Not sure if emulator-proxy needs to have access to CAN Network
        networks = self._config_model.required_networks
        self._logging_client.log_networks(networks)
        return networks

    def generate_build(self) -> Optional[BuildItem]:
        repo = OpentronsRepository.OPENTRONS
        build_args = get_build_args(
            repo,
            "latest",
            self._global_settings.get_repo_commit(repo),
            self._global_settings.get_repo_head(repo),
        )
        self._logging_client.log_build(build_args)
        return get_service_build(self._image, build_args, self._dev)

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        volumes = None
        self._logging_client.log_volumes(volumes)
        return volumes

    def generate_command(self) -> Optional[IntermediateCommand]:
        command = None
        self._logging_client.log_command(command)
        return command

    def generate_ports(self) -> Optional[IntermediatePorts]:
        ports = None
        self._logging_client.log_ports(ports)
        return ports

    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        depends_on = None
        self._logging_client.log_depends_on(depends_on)
        return depends_on

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        env_vars = {
            env_var_name: env_var_value
            for module in self.MODULE_TYPES
            for env_var_name, env_var_value in module.get_proxy_info_env_var().items()  # type: ignore [attr-defined]
        }
        self._logging_client.log_env_vars(env_vars)
        return env_vars
