"""Custom type aliases to add a nice layer of abstraction."""
from typing import Union

from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    OT2Model,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)

Modules = Union[
    HeaterShakerModuleInputModel,
    ThermocyclerModuleInputModel,
    TemperatureModuleInputModel,
    MagneticModuleInputModel,
]

Robots = Union[OT2Model]

Containers = Union[Robots, Modules]
