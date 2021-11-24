from enum import Enum
from typing_extensions import Literal
from compose_file_creator.input.models.container_types.base_attributes import (
    BaseAttributes
)
from compose_file_creator.input.settings import (
    Hardware,
    HeaterShakerModes
)


class HeaterShakerModuleAttributes(BaseAttributes):
    hardware: Literal[Hardware.HEATER_SHAKER_MODULE.value]
    mode: HeaterShakerModes = HeaterShakerModes.SOCKET
