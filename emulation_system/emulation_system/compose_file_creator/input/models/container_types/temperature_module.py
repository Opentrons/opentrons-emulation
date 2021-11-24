from pydantic import Field
from typing_extensions import Literal
from compose_file_creator.input.models.container_types.base_attributes import (
    BaseAttributes
)
from compose_file_creator.input.settings import Hardware, TemperatureModelSettings


class TemperatureModuleAttributes(BaseAttributes):
    hardware: Literal[Hardware.TEMPERATURE_MODULE.value]
    temperature: TemperatureModelSettings = TemperatureModelSettings()