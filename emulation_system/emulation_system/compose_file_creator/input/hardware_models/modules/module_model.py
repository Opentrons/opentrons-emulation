"""Parent class of all Modules, Subclass of HardwareModel.

Used to group all modules together and distinguish them from robots.
"""
import json
from typing import (
    ClassVar,
    Dict,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)

from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
    EmulationLevelNotSupportedError,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
)


class FirmwareSerialNumberModel(BaseModel):
    """Model for information needed to set a firmware emulator's serial number."""

    model: str
    version: str
    env_var_name: str


class ModuleInputModel(HardwareModel):
    """Parent class of all Modules, Subclass of HardwareModel.

    Used to group all modules together and distinguish them from robots.
    """

    firmware_serial_number_info: ClassVar[Optional[FirmwareSerialNumberModel]] = Field(
        alias="firmware-serial-number-info", allow_mutation=False
    )

    def _get_firmware_serial_number_env_var(self) -> Dict[str, str]:
        """Builds firmware level serial number environment variable."""
        if self.firmware_serial_number_info is None:
            raise EmulationLevelNotSupportedError(
                f'Emulation level, "{self.emulation_level}" not supported for '
                f"{self.hardware}"
            )
        value = {
            "serial_number": self.id,
            "model": self.firmware_serial_number_info.model,
            "version": self.firmware_serial_number_info.version,
        }
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
