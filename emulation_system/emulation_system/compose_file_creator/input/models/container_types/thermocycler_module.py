from pydantic import Field

from typing_extensions import Literal
from compose_file_creator.input.models.container_types.base_attributes import (
    BaseAttributes
)
from compose_file_creator.input.settings import Hardware, TemperatureModelSettings


class ThermocyclerModuleAttributes(BaseAttributes):
    hardware: Literal[Hardware.THERMOCYCLER_MODULE.value]
    lid_temperature: TemperatureModelSettings = Field(
        alias="lid-temperature", default=TemperatureModelSettings()
    )
    plate_temperature: TemperatureModelSettings = Field(
        alias="plate-temperature", default=TemperatureModelSettings()
    )
