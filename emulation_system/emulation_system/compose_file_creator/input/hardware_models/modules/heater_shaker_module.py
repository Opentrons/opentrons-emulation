"""Model and attributes for heater-shaker Module."""
from typing import ClassVar, List, Optional

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    ModuleInputModel,
    ProxyInfoModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    HeaterShakerModes,
    OpentronsRepository,
    SourceRepositories,
)


class HeaterShakerModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Heater Shaker Module."""

    mode: HeaterShakerModes = HeaterShakerModes.SOCKET

    class Config:  # noqa: D106
        use_enum_values = True


class HeaterShakerModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: Literal[None] = None
    hardware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS_MODULES


class HeaterShakerModuleInputModel(ModuleInputModel):
    """Model for Heater Shaker Module."""

    # Not defined because Heater Shaker does not have a firmware level implementation
    firmware_serial_number_info: ClassVar[Literal[None]] = None
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
        alias="hardware-specific-attributes", default=HeaterShakerModuleAttributes()
    )
    emulation_level: Literal[EmulationLevels.HARDWARE] = Field(alias="emulation-level")

    def get_hardware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for heater shaker when it is being emulated at hardware level."""
        return [
            "--socket",
            f"http://{emulator_proxy_name}:{self.proxy_info.emulator_port}",
        ]
