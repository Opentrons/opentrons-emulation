from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    Command,
    DependsOn,
    EnvironmentVariables,
    Ports,
    RequiredNetworks,
    Volumes,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Service,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)


class AbstractServiceBuilder(ABC):
    """Abstract class defining all necessary functions to build a service."""

    @abstractmethod
    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
    ) -> None:
        self._config_model = config_model
        self._global_settings = global_settings

    @staticmethod
    def _generate_container_name(
        container_id: str, system_unique_id: Optional[str]
    ) -> str:
        container_name = (
            f"{system_unique_id}-{container_id}"
            if system_unique_id is not None
            else container_id
        )
        return container_name

    @abstractmethod
    def generate_image(self) -> str:
        ...

    @abstractmethod
    def is_tty(self) -> bool:
        ...

    @abstractmethod
    def generate_networks(self) -> RequiredNetworks:
        ...

    #############################################################
    # The following generate_* methods optionally return values #
    #############################################################

    @abstractmethod
    def generate_build(self) -> Optional[BuildItem]:
        ...

    @abstractmethod
    def generate_volumes(self) -> Optional[Volumes]:
        ...

    @abstractmethod
    def generate_ports(self) -> Optional[Ports]:
        ...

    @abstractmethod
    def generate_env_vars(self) -> Optional[EnvironmentVariables]:
        ...

    @abstractmethod
    def generate_command(self) -> Optional[Command]:
        ...

    @abstractmethod
    def generate_depends_on(self) -> Optional[DependsOn]:
        ...

    def build_service(self) -> Service:
        return Service(
            container_name=self.generate_container_name(),
            image=self.generate_image(),
            build=self.generate_build(),
            tty=self.is_tty(),
            networks=self.generate_networks(),
            volumes=self.generate_volumes(),
            ports=self.generate_ports(),
            environment=self.generate_env_vars(),
            command=self.generate_command(),
            depends_on=self.generate_depends_on(),
        )
