from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, cast

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.docker_expected_types import (
    ServiceBuild,
    ServiceCommand,
    ServiceContainerName,
    ServiceEnvironment,
    ServiceImage,
    ServicePorts,
    ServiceTTY,
    ServiceVolumes,
)
from emulation_system.intermediate_types import (
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
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
    def generate_container_name(self) -> str:
        ...

    @abstractmethod
    def generate_image(self) -> str:
        ...

    @abstractmethod
    def is_tty(self) -> bool:
        ...

    @abstractmethod
    def generate_networks(self) -> IntermediateNetworks:
        ...

    #############################################################
    # The following generate_* methods optionally return values #
    #############################################################

    @abstractmethod
    def generate_build(self) -> Optional[BuildItem]:
        ...

    @abstractmethod
    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        ...

    @abstractmethod
    def generate_ports(self) -> Optional[IntermediatePorts]:
        ...

    @abstractmethod
    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        ...

    @abstractmethod
    def generate_command(self) -> Optional[IntermediateCommand]:
        ...

    @abstractmethod
    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        ...

    def build_service(self) -> Service:
        return Service(
            container_name=cast(ServiceContainerName, self.generate_container_name()),
            image=cast(ServiceImage, self.generate_image()),
            build=cast(ServiceBuild, self.generate_build()),
            tty=cast(ServiceTTY, self.is_tty()),
            volumes=cast(ServiceVolumes, self.generate_volumes()),
            ports=cast(ServicePorts, self.generate_ports()),
            environment=cast(ServiceEnvironment, self.generate_env_vars()),
            command=cast(ServiceCommand, self.generate_command()),
            networks=self.generate_networks(),
            depends_on=self.generate_depends_on(),
        )
