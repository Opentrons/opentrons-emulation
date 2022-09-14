"""Parent class of all Modules, Subclass of HardwareModel.

Used to group all modules together and distinguish them from robots.
"""
import json
from typing import ClassVar, Dict, Optional

from pydantic import BaseModel, Field

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
)

from ..hardware_model import EmulationLevelNotSupportedError, HardwareModel


class FirmwareSerialNumberModel(BaseModel):
    """Model for information needed to set a firmware emulator's serial number."""

    env_var_name: str
    model: str
    version: str


class ProxyInfoModel(BaseModel):
    """Model to provide information needed to connect module to proxy."""

    env_var_name: str
    emulator_port: int
    driver_port: int


class ModuleInputModel(HardwareModel):
    """Parent class of all Modules, Subclass of HardwareModel.

    Used to group all modules together and distinguish them from robots.
    """

    firmware_serial_number_info: ClassVar[Optional[FirmwareSerialNumberModel]] = Field(
        alias="firmware-serial-number-info", allow_mutation=False
    )
    proxy_info: ClassVar[ProxyInfoModel] = Field(
        alias="proxy-info", allow_mutation=False
    )

    def _get_firmware_serial_number_env_var(self) -> Dict[str, str]:
        """Builds firmware level serial number environment variable."""
        if self.firmware_serial_number_info is None:
            raise EmulationLevelNotSupportedError(self.emulation_level, self.hardware)
        value = {
            "serial_number": self.id,
            "model": self.firmware_serial_number_info.model,
            "version": self.firmware_serial_number_info.version,
        }

        if self.hardware in [
            Hardware.THERMOCYCLER_MODULE,
            Hardware.TEMPERATURE_MODULE,
            Hardware.HEATER_SHAKER_MODULE,
        ]:
            value.update(self.hardware_specific_attributes.dict())

        return {self.firmware_serial_number_info.env_var_name: json.dumps(value)}

    def _get_hardware_serial_number_env_var(self) -> Dict[str, str]:
        """Builds hardware level serial number environment variable."""
        return {"SERIAL_NUMBER": self.id}

    def get_serial_number_env_var(self) -> Dict[str, str]:
        """Builds serial number env var based off of emulation level."""
        return (
            self._get_firmware_serial_number_env_var()
            if self.emulation_level == EmulationLevels.FIRMWARE
            else self._get_hardware_serial_number_env_var()
        )

    @classmethod
    def get_proxy_info_env_var(cls) -> Dict[str, str]:
        """Builds proxy info env var."""
        value = {
            "emulator_port": cls.proxy_info.emulator_port,
            "driver_port": cls.proxy_info.driver_port,
        }
        return {cls.proxy_info.env_var_name: json.dumps(value)}
