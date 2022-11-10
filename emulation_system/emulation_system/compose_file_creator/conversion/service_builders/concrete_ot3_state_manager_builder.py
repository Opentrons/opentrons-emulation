"""Module containing ConcreteOT3ServiceBuilder class."""
from typing import Optional

from emulation_system import (
    OpentronsEmulationConfiguration,
    SystemConfigurationModel,
)
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
    get_build_args,
)
from .abstract_service_builder import AbstractServiceBuilder


class ConcreteOT3StateManagerBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building OT-3 State Manager Service."""

    IMAGE_NAME = "ot3-state-manager"
    CONTAINER_NAME = IMAGE_NAME

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Instantiates a ConcreteOT3ServiceBuilder object."""
        super().__init__(config_model, global_settings, dev)
        self._ot3 = self.get_ot3(config_model)

    @property
    def _image(self) -> str:
        return self.IMAGE_NAME

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self.CONTAINER_NAME, system_unique_id
        )
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return self.IMAGE_NAME

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        tty = True
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        networks = self._config_model.required_networks
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
                self._global_settings.get_repo_commit(ot3_firmware_repo),
                self._global_settings.get_repo_head(ot3_firmware_repo),
            )
            build_args.update(ot3_firmware_build_args)

        if self._ot3.opentrons_hardware_source_type == SourceType.REMOTE:
            monorepo_build_args = get_build_args(
                monorepo,
                self._ot3.opentrons_hardware_source_location,
                self._global_settings.get_repo_commit(monorepo),
                self._global_settings.get_repo_head(monorepo),
            )
            build_args.update(monorepo_build_args)

        return build_args if len(build_args) > 0 else None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        return None

    def generate_command(self) -> Optional[IntermediateCommand]:
        """Generates value for command parameter."""
        command = None
        return command

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        return self._ot3.get_ot3_state_manager_bound_port()

    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        """Generates value for depends_on parameter."""
        depends_on = None

        return depends_on

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        return (
            self._ot3.state_manager_env_vars
            if self._ot3.state_manager_env_vars is not None
            else None
        )
