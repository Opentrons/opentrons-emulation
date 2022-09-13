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
    Command,
    DependsOn,
    EnvironmentVariables,
    Ports,
    RequiredNetworks,
    Volumes,
)


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
        self._image = self._generate_image()

    def generate_container_name(self) -> str:
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self.EMULATOR_PROXY_NAME, system_unique_id
        )
        return container_name

    @staticmethod
    def _generate_image() -> str:
        return EmulatorProxyImages().remote_firmware_image_name

    def generate_image(self) -> str:
        return get_service_image(self._image)

    def is_tty(self) -> bool:
        tty = True
        return tty

    def generate_networks(self) -> RequiredNetworks:
        networks = self._config_model.required_networks
        return networks

    def generate_build(self) -> Optional[BuildItem]:
        repo = OpentronsRepository.OPENTRONS
        build_args = get_build_args(
            repo,
            "latest",
            self._global_settings.get_repo_commit(repo),
            self._global_settings.get_repo_head(repo),
        )
        return get_service_build(self._image, build_args, self._dev)

    def generate_volumes(self) -> Optional[Volumes]:
        return None

    def generate_command(self) -> Optional[Command]:
        return None

    def generate_ports(self) -> Optional[Ports]:
        return None

    def generate_depends_on(self) -> Optional[DependsOn]:
        return None

    def generate_env_vars(self) -> Optional[EnvironmentVariables]:
        return {
            env_var_name: env_var_value
            for module in self.MODULE_TYPES
            for env_var_name, env_var_value in module.get_proxy_info_env_var().items()
        }
