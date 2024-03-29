"""Model and attributes for Magnetic Module."""
from typing import ClassVar

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceRepositories,
)

from ..hardware_specific_attributes import HardwareSpecificAttributes
from .module_model import FirmwareSerialNumberModel, ModuleInputModel, ProxyInfoModel


class MagneticModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Magnetic Module."""

    pass


class MagneticModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: Literal[None] = None


class MagneticModuleInputModel(ModuleInputModel):
    """Model for Magnetic Module."""

    firmware_serial_number_info: ClassVar[
        FirmwareSerialNumberModel
    ] = FirmwareSerialNumberModel(
        model="mag_deck_v20", version="2.0.0", env_var_name="OT_EMULATOR_magdeck"
    )
    proxy_info: ClassVar[ProxyInfoModel] = ProxyInfoModel(
        env_var_name="OT_EMULATOR_magdeck_proxy",
        emulator_port=10002,
        driver_port=11002,
    )

    hardware: Literal[Hardware.MAGNETIC_MODULE]
    source_repos: MagneticModuleSourceRepositories = Field(
        default=MagneticModuleSourceRepositories(), const=True, exclude=True
    )
    hardware_specific_attributes: MagneticModuleAttributes = Field(
        default=MagneticModuleAttributes()
    )
    emulation_level: Literal[EmulationLevels.FIRMWARE]

    def get_module_args(self, emulator_proxy_name: str) -> str:
        """Get module args for Magnetic Module."""
        return emulator_proxy_name
