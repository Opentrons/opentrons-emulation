"""Model and attributes for heater-shaker Module."""
from typing import ClassVar

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    HeaterShakerModes,
    OpentronsRepository,
    RPMModelSettings,
    SourceRepositories,
    TemperatureModelSettings,
)

from ..hardware_specific_attributes import HardwareSpecificAttributes
from .module_model import FirmwareSerialNumberModel, ModuleInputModel, ProxyInfoModel


class HeaterShakerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Heater Shaker Module."""

    mode: HeaterShakerModes = HeaterShakerModes.SOCKET
    temperature: TemperatureModelSettings = Field(default=TemperatureModelSettings())
    rpm: RPMModelSettings = Field(default=RPMModelSettings())

    class Config:  # noqa: D106
        use_enum_values = True


class HeaterShakerModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS_MODULES


class HeaterShakerModuleInputModel(ModuleInputModel):
    """Model for Heater Shaker Module."""

    # Not defined because Heater Shaker does not have a firmware level implementation
    firmware_serial_number_info: ClassVar[
        FirmwareSerialNumberModel
    ] = FirmwareSerialNumberModel(
        model="v01", version="v0.0.1", env_var_name="OT_EMULATOR_heatershaker"
    )
    proxy_info: ClassVar[ProxyInfoModel] = ProxyInfoModel(
        env_var_name="OT_EMULATOR_heatershaker_proxy",
        emulator_port=10004,
        driver_port=11004,
    )

    hardware: Literal[Hardware.HEATER_SHAKER_MODULE]
    source_repos: HeaterShakerModuleSourceRepositories = Field(
        default=HeaterShakerModuleSourceRepositories(), const=True, exclude=True
    )
    hardware_specific_attributes: HeaterShakerModuleAttributes = Field(
        default=HeaterShakerModuleAttributes()
    )
    emulation_level: Literal[EmulationLevels.HARDWARE, EmulationLevels.FIRMWARE]

    def get_module_args(self, emulator_proxy_name: str) -> str:
        """Get module args for Heater-Shaker."""
        if self.emulation_level == EmulationLevels.HARDWARE:
            return (
                f"--socket http://{emulator_proxy_name}:{self.proxy_info.emulator_port}"
            )
        else:
            return emulator_proxy_name
