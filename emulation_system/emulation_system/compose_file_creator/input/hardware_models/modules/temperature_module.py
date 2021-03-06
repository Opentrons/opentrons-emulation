"""Model and attributes for Temperature Module."""
from typing import ClassVar, List, Optional

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    FirmwareSerialNumberModel,
    ModuleInputModel,
    ProxyInfoModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceRepositories,
    TemperatureModelSettings,
)


class TemperatureModuleAttributes(HardwareSpecificAttributes):
    """Attributes specific to Temperature Module."""

    temperature: TemperatureModelSettings = TemperatureModelSettings()


class TemperatureModuleSourceRepositories(SourceRepositories):
    """Source repositories for Heater-Shaker."""

    firmware_repo_name: OpentronsRepository = OpentronsRepository.OPENTRONS
    hardware_repo_name: Literal[None] = None


class TemperatureModuleInputModel(ModuleInputModel):
    """Model for Temperature Module."""

    firmware_serial_number_info: ClassVar[
        FirmwareSerialNumberModel
    ] = FirmwareSerialNumberModel(
        model="temp_deck_v20", version="v2.0.1", env_var_name="OT_EMULATOR_tempdeck"
    )
    proxy_info: ClassVar[ProxyInfoModel] = ProxyInfoModel(
        env_var_name="OT_EMULATOR_temperature_proxy",
        emulator_port=10001,
        driver_port=11001,
    )

    hardware: Literal[Hardware.TEMPERATURE_MODULE]
    source_repos: TemperatureModuleSourceRepositories = Field(
        default=TemperatureModuleSourceRepositories(), const=True, exclude=True
    )
    hardware_specific_attributes: TemperatureModuleAttributes = Field(
        alias="hardware-specific-attributes", default=TemperatureModuleAttributes()
    )

    emulation_level: Literal[EmulationLevels.FIRMWARE] = Field(alias="emulation-level")

    def get_firmware_level_command(
        self, emulator_proxy_name: str
    ) -> Optional[List[str]]:
        """Get command for module when it is being emulated at hardware level."""
        return [emulator_proxy_name]
