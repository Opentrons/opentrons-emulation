from emulation_system.compose_file_creator.input.models.hardware_specific_attributes.base_type import HardwareSpecificAttributes
from emulation_system.compose_file_creator.input.settings import (
    HeaterShakerModes
)


class HeaterShakerModuleAttributes(HardwareSpecificAttributes):
    mode: HeaterShakerModes = HeaterShakerModes.SOCKET
