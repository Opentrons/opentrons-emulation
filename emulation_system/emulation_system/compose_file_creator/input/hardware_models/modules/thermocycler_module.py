"""Model and attributes for Thermocycler Module."""
from typing import ClassVar

from pydantic import Field
from typing_extensions import Literal

from emulation_system.compose_file_creator.input.hardware_models.hardware_specific_attributes import (  # noqa: E501
    HardwareSpecificAttributes,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    FirmwareSerialNumberModel,
    ModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
    SourceRepositories,
    TemperatureModelSettings,
)


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

    hardware: Literal[Hardware.THERMOCYCLER_MODULE]
    source_repos: ThermocyclerModuleSourceRepositories = Field(
        default=ThermocyclerModuleSourceRepositories(), const=True
    )
    hardware_specific_attributes: ThermocyclerModuleAttributes = Field(
        alias="hardware-specific-attributes", default=ThermocyclerModuleAttributes()
    )
    emulation_level: Literal[
        EmulationLevels.FIRMWARE, EmulationLevels.HARDWARE
    ] = Field(alias="emulation-level")
