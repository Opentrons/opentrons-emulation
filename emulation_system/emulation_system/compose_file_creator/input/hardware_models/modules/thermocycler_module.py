"""Model and attributes for Thermocycler Module."""
from typing import (
    ClassVar,
    List,
    Optional,
)

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceRepositories,
    TemperatureModelSettings,
)
from .module_model import (
    FirmwareSerialNumberModel,
    ModuleInputModel,
    ProxyInfoModel,
)
from ..hardware_specific_attributes import HardwareSpecificAttributes


class ThermocyclerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Thermocycler module."""

    lid_temperature: TemperatureModelSettings = Field(
        alias="lid-temperature", default=TemperatureModelSettings()
    )
    plate_temperature: TemperatureModelSettings = Field(
        alias="plate-temperature", default=TemperatureModelSettings()
    )


class ThermocyclerModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS_MODULES


class ThermocyclerModuleInputModel(ModuleInputModel):
    """Model for Thermocycler Module."""

    firmware_serial_number_info: ClassVar[
        FirmwareSerialNumberModel
    ] = FirmwareSerialNumberModel(
        model="v02", version="v1.1.0", env_var_name="OT_EMULATOR_thermocycler"
    )
    proxy_info: ClassVar[ProxyInfoModel] = ProxyInfoModel(
        env_var_name="OT_EMULATOR_thermocycler_proxy",
        emulator_port=10003,
        driver_port=11003,
    )

    hardware: Literal[Hardware.THERMOCYCLER_MODULE]
    source_repos: ThermocyclerModuleSourceRepositories = Field(
        default=ThermocyclerModuleSourceRepositories(), const=True, exclude=True
    )
    hardware_specific_attributes: ThermocyclerModuleAttributes = Field(
        alias="hardware-specific-attributes", default=ThermocyclerModuleAttributes()
    )
    emulation_level: Literal[
        EmulationLevels.FIRMWARE, EmulationLevels.HARDWARE
    ] = Field(alias="emulation-level")

    def get_hardware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for heater shaker when it is being emulated at hardware level."""
        return [
            f"--socket http://{emulator_proxy_name}:{self.proxy_info.emulator_port}",
        ]

    def get_firmware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for module when it is being emulated at hardware level."""
        return [emulator_proxy_name]
