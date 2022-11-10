"""Module containing ServiceBuilderOrchestrator class."""
from typing import List, Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import Service

from ...config_file_settings import OT3Hardware
from ...images import (
    OT3BootloaderImages,
    OT3GantryXImages,
    OT3GantryYImages,
    OT3GripperImages,
    OT3HeadImages,
    OT3PipettesImages,
)
from ...types.intermediate_types import DockerServices
from . import (
    ConcreteCANServerServiceBuilder,
    ConcreteEmulatorProxyServiceBuilder,
    ConcreteInputServiceBuilder,
    ConcreteOT3ServiceBuilder,
    ConcreteOT3StateManagerBuilder,
    ConcreteSmoothieServiceBuilder,
)
from .service_info import ServiceInfo


class ServiceBuilderOrchestrator:
    """Class that client uses to interface with builders."""

    OT3_SERVICES_TO_CREATE = [
        ServiceInfo(OT3HeadImages(), OT3Hardware.HEAD),
        ServiceInfo(OT3PipettesImages(), OT3Hardware.PIPETTES),
        ServiceInfo(OT3GantryXImages(), OT3Hardware.GANTRY_X),
        ServiceInfo(OT3GantryYImages(), OT3Hardware.GANTRY_Y),
        ServiceInfo(OT3BootloaderImages(), OT3Hardware.BOOTLOADER),
        ServiceInfo(OT3GripperImages(), OT3Hardware.GRIPPER),
    ]

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Instantiates a ServiceBuilderOrchestrator object."""
        self._config_model = config_model
        self._global_settings = global_settings
        self._dev = dev
        self._services: DockerServices = {}

    def _build_can_server_service(self) -> Service:
        """Method to generate and return a CAN Server Service."""
        return ConcreteCANServerServiceBuilder(
            self._config_model, self._global_settings, self._dev
        ).build_service()

    def _build_emulator_proxy_service(self) -> Service:
        """Method to generate and return an Emulator Proxy Service."""
        return ConcreteEmulatorProxyServiceBuilder(
            self._config_model, self._global_settings, self._dev
        ).build_service()

    def _build_smoothie_service(self) -> Service:
        """Method to generate and return a Smoothie Service."""
        return ConcreteSmoothieServiceBuilder(
            self._config_model, self._global_settings, self._dev
        ).build_service()

    def _build_ot3_services(
        self, can_server_service_name: str, state_manager_name: str
    ) -> List[Service]:
        """Generates OT-3 Firmware Services."""
        return [
            ConcreteOT3ServiceBuilder(
                self._config_model,
                self._global_settings,
                self._dev,
                can_server_service_name,
                state_manager_name,
                service_info,
            ).build_service()
            for service_info in self.OT3_SERVICES_TO_CREATE
        ]

    def _build_ot3_state_manager_service(self) -> Service:
        return ConcreteOT3StateManagerBuilder(
            self._config_model, self._global_settings, self._dev
        ).build_service()

    def _build_input_services(
        self,
        emulator_proxy_name: Optional[str],
        smoothie_name: Optional[str],
        can_server_service_name: Optional[str],
    ) -> List[Service]:
        """Build services directly specified in input file."""
        return [
            ConcreteInputServiceBuilder(
                self._config_model,
                self._global_settings,
                self._dev,
                container,
                emulator_proxy_name,
                smoothie_name,
                can_server_service_name,
            ).build_service()
            for container in self._config_model.containers.values()
        ]

    def __add_ot2_services(self) -> str:
        smoothie_service = self._build_smoothie_service()
        smoothie_name = smoothie_service.container_name
        assert smoothie_name is not None
        self._services[smoothie_name] = smoothie_service

        return smoothie_name

    def __add_ot3_services(self) -> str:
        can_server_service = self._build_can_server_service()
        can_server_service_name = can_server_service.container_name
        ot3_state_manager_service = self._build_ot3_state_manager_service()
        ot3_state_manager_service_name = ot3_state_manager_service.container_name

        assert can_server_service_name is not None
        assert ot3_state_manager_service_name is not None

        ot3_services = self._build_ot3_services(
            can_server_service_name, ot3_state_manager_service_name
        )
        self._services[can_server_service_name] = can_server_service
        self._services[ot3_state_manager_service_name] = ot3_state_manager_service
        for ot3_service in ot3_services:
            assert ot3_service.container_name is not None
            self._services[ot3_service.container_name] = ot3_service

        return can_server_service_name

    def __add_emulator_proxy_service(self) -> str:
        emulator_proxy_service = self._build_emulator_proxy_service()
        emulator_proxy_name = emulator_proxy_service.container_name
        assert emulator_proxy_name is not None  # For mypy
        self._services[emulator_proxy_name] = emulator_proxy_service

        return emulator_proxy_name

    def __add_input_services(
        self,
        emulator_proxy_name: str,
        smoothie_name: Optional[str],
        can_server_service_name: Optional[str],
    ) -> None:
        input_services = self._build_input_services(
            emulator_proxy_name, smoothie_name, can_server_service_name
        )
        for service in input_services:
            assert service.container_name is not None
            self._services[service.container_name] = service

    def __add_local_ot3_builder(self) -> None:
        print("Local ot3-firmware builder required")

    def __add_local_opentrons_modules_builder(self) -> None:
        print("Local opentrons-modules builder required")

    def __add_local_monorepo_builder(self) -> None:
        print("Local monorepo builder required")

    def build_services(self) -> DockerServices:
        """Build services."""
        emulator_proxy_name = self.__add_emulator_proxy_service()
        smoothie_name = (
            self.__add_ot2_services() if self._config_model.has_ot2 else None
        )
        can_server_service_name = (
            self.__add_ot3_services() if self._config_model.has_ot3 else None
        )
        self.__add_input_services(
            emulator_proxy_name, smoothie_name, can_server_service_name
        )
        if self._config_model.local_ot3_builder_required:
            self.__add_local_ot3_builder()

        if self._config_model.local_opentrons_modules_builder_required:
            self.__add_local_opentrons_modules_builder()

        if self._config_model.local_monorepo_builder_required:
            self.__add_local_monorepo_builder()

        return DockerServices(self._services)
