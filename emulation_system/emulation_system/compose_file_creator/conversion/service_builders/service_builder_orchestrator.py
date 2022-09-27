"""Module containing ServiceBuilderOrchestrator class."""
from typing import List

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
from . import (
    ConcreteCANServerServiceBuilder,
    ConcreteEmulatorProxyServiceBuilder,
    ConcreteOT3ServiceBuilder,
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

    def build_can_server_service(self) -> Service:
        """Method to generate and return a CAN Server Service."""
        return ConcreteCANServerServiceBuilder(
            self._config_model, self._global_settings, self._dev
        ).build_service()

    def build_emulator_proxy_service(self) -> Service:
        """Method to generate and return an Emulator Proxy Service."""
        return ConcreteEmulatorProxyServiceBuilder(
            self._config_model, self._global_settings, self._dev
        ).build_service()

    def build_smoothie_service(self) -> Service:
        """Method to generate and return a Smoothie Service."""
        return ConcreteSmoothieServiceBuilder(
            self._config_model, self._global_settings, self._dev
        ).build_service()

    def build_ot3_services(self, can_server_service_name: str) -> List[Service]:
        """Generates OT-3 Firmware Services."""
        return [
            ConcreteOT3ServiceBuilder(
                self._config_model,
                self._global_settings,
                self._dev,
                can_server_service_name,
                service_info,
            ).build_service()
            for service_info in self.OT3_SERVICES_TO_CREATE
        ]
