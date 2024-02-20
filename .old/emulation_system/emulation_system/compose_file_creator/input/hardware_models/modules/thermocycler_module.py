"""Model and attributes for Thermocycler Module."""
from typing import ClassVar

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceRepositories,
    TemperatureModelSettings,
)

from ..hardware_specific_attributes import HardwareSpecificAttributes
from .module_model import FirmwareSerialNumberModel, ModuleInputModel, ProxyInfoModel


class ThermocyclerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Thermocycler module."""

    lid_temperature: TemperatureModelSettings = Field(
        default=TemperatureModelSettings()
    )
    plate_temperature: TemperatureModelSettings = Field(
        default=TemperatureModelSettings()
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
        default=ThermocyclerModuleAttributes()
    )
    emulation_level: Literal[EmulationLevels.FIRMWARE, EmulationLevels.HARDWARE]

    def get_module_args(self, emulator_proxy_name: str) -> str:
        """Get module args for Thermocycler."""
        if self.emulation_level == EmulationLevels.HARDWARE:
            return (
                f"--socket http://{emulator_proxy_name}:{self.proxy_info.emulator_port}"
            )

        else:
            return emulator_proxy_name
