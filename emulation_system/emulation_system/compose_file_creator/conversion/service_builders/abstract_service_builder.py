"""Module containing AbstractServiceBuilder class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Type, cast

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.config_file_settings import Hardware
from emulation_system.compose_file_creator.errors import (
    HardwareDoesNotExistError,
    IncorrectHardwareError,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    OT2InputModel,
    OT3InputModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import ListOrDict
from emulation_system.compose_file_creator.types.final_types import (
    ServiceBuild,
    ServiceCommand,
    ServiceContainerName,
    ServiceEnvironment,
    ServiceImage,
    ServicePorts,
    ServiceTTY,
    ServiceVolumes,
)
from emulation_system.compose_file_creator.types.input_types import Robots
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.compose_file_creator.utilities.hardware_utils import (
    is_ot2,
    is_ot3,
)
from emulation_system.consts import (
    DEV_DOCKERFILE_NAME,
    DOCKERFILE_DIR_LOCATION,
    DOCKERFILE_NAME,
)


class AbstractServiceBuilder(ABC):
    """Abstract class defining all necessary functions to build a service."""

    @abstractmethod
    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
    ) -> None:
        """Defines parameters required for ALL concrete builders."""
        self._config_model = config_model
        self._global_settings = global_settings
        self._image: str = NotImplemented
        self._dev: bool = NotImplemented

    @staticmethod
    def _get_robot(
        config_model: SystemConfigurationModel,
        hardware: Hardware,
        expected_type: Type[Robots],
    ) -> Robots:
        """Checks for robot object in SystemConfigurationModel and returns it."""
        robot = config_model.robot
        if robot is None:
            raise HardwareDoesNotExistError(hardware)
        if not isinstance(robot, expected_type):
            raise IncorrectHardwareError(robot.hardware, hardware)
        return robot

    @classmethod
    def get_ot2(cls, config_model: SystemConfigurationModel) -> OT2InputModel:
        """Checks for OT-2 object in SystemConfigurationModel and returns it."""
        robot = cls._get_robot(config_model, Hardware.OT2, OT2InputModel)
        assert is_ot2(robot)
        return robot

    @classmethod
    def get_ot3(cls, config_model: SystemConfigurationModel) -> OT3InputModel:
        """Checks for OT-3 object in SystemConfigurationModel and returns it."""
        robot = cls._get_robot(config_model, Hardware.OT3, OT3InputModel)
        assert is_ot3(robot)
        return robot

    @staticmethod
    def _generate_container_name(
        container_id: str, system_unique_id: Optional[str]
    ) -> str:
        """Generates container_name.

        Looks at system-unique-id field from configuration file.
        If it exists, prepends it to passed container-id and returns new value.
        If it does not exist, just returns container-id.
        """
        container_name = (
            f"{system_unique_id}-{container_id}"
            if system_unique_id is not None
            else container_id
        )
        return container_name

    @abstractmethod
    def generate_container_name(self) -> str:
        """Method to generate value for container_name parameter for Service."""
        ...

    @abstractmethod
    def generate_image(self) -> str:
        """Method to generate value for image parameter for Service."""
        ...

    @abstractmethod
    def is_tty(self) -> bool:
        """Method to generate value for tty parameter for Service."""
        ...

    @abstractmethod
    def generate_networks(self) -> IntermediateNetworks:
        """Method to generate value for networks parameter for Service."""
        ...

    #############################################################
    # The following generate_* methods optionally return values #
    #############################################################

    @abstractmethod
    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Method to, if necessary, generate value for build parameter for Service."""
        ...

    def generate_build(self) -> BuildItem:
        """Generates BuildItem."""
        return BuildItem(
            context=DOCKERFILE_DIR_LOCATION,
            target=self._image,
            args=cast(ListOrDict, self.generate_build_args()),
            dockerfile=DEV_DOCKERFILE_NAME if self._dev else DOCKERFILE_NAME,
        )

    @abstractmethod
    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Method to, if necessary, generate value for volumes parameter for Service."""
        ...

    @abstractmethod
    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Method to, if necessary, generate value for ports parameter for Service."""
        ...

    @abstractmethod
    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Method to, if necessary, generate value for environment parameter for Service."""
        ...

    @abstractmethod
    def generate_command(self) -> Optional[IntermediateCommand]:
        """Method to, if necessary, generate value for command parameter for Service."""
        ...

    @abstractmethod
    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        """Method to, if necessary, generate value for depends_on parameter for Service."""
        ...

    def build_service(self) -> Service:
        """Method calling all generate* methods to build Service object."""
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
