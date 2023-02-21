"""Module containing AbstractService class."""

from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod
from typing import Optional, Type, cast

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.config_file_settings import (
    FileMount,
    Hardware,
    MountTypes,
)
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
    ServiceContainerName,
    ServiceEnvironment,
    ServiceHealthcheck,
    ServiceImage,
    ServicePorts,
    ServiceTTY,
    ServiceVolumes,
)
from emulation_system.compose_file_creator.types.input_types import Robots
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
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
    ENTRYPOINT_FILE_LOCATION,
)
from emulation_system.source import (
    MonorepoSource,
    OpentronsModulesSource,
    OT3FirmwareSource,
)


class AbstractService(ABC):
    """Abstract class defining all necessary functions to build a service."""

    ENTRYPOINT_MOUNT_STRING = FileMount(
        type=MountTypes.FILE,
        source_path=pathlib.Path(ENTRYPOINT_FILE_LOCATION),
        mount_path="/entrypoint.sh",
    ).get_bind_mount_string()

    @abstractmethod
    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Defines parameters required for ALL concrete builders."""
        self._config_model = config_model
        self._global_settings = global_settings
        self._dev = dev

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

    @property
    def _ot3_source(self) -> OT3FirmwareSource:
        return self._config_model.ot3_firmware_source

    @property
    def _monorepo_source(self) -> MonorepoSource:
        return self._config_model.monorepo_source

    @property
    def _opentrons_modules_source(self) -> OpentronsModulesSource:
        return self._config_model.opentrons_modules_source

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

    @property
    @abstractmethod
    def _image(self) -> str:
        ...

    @staticmethod
    def _generate_container_name(
        container_id: str, system_unique_id: Optional[str]
    ) -> str:
        """Generates container_name.

        Looks at system-unique-id field from configuration file.
        If it exists, prepends it to passed container-id and returns new value.
        If it does not exist, just returns container-id.
        """
        return (
            f"{system_unique_id}-{container_id}"
            if system_unique_id is not None
            else container_id
        )

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

    @abstractmethod
    def generate_healthcheck(self) -> Optional[IntermediateHealthcheck]:
        """Method to generate value for healthcheck parameter on Service."""
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

    def build_service(self) -> Service:
        """Method calling all generate* methods to build Service object."""
        intermediate_healthcheck = self.generate_healthcheck()

        return Service(
            container_name=cast(ServiceContainerName, self.generate_container_name()),
            image=cast(ServiceImage, self.generate_image()),
            build=cast(ServiceBuild, self.generate_build()),
            tty=cast(ServiceTTY, self.is_tty()),
            volumes=cast(ServiceVolumes, self.generate_volumes()),
            ports=cast(ServicePorts, self.generate_ports()),
            environment=cast(ServiceEnvironment, self.generate_env_vars()),
            networks=self.generate_networks(),
            healthcheck=ServiceHealthcheck(
                interval=f"{intermediate_healthcheck.interval}s",
                retries=intermediate_healthcheck.retries,
                timeout=f"{intermediate_healthcheck.timeout}s",
                test=intermediate_healthcheck.command,
            )
            if intermediate_healthcheck is not None
            else None,
        )
