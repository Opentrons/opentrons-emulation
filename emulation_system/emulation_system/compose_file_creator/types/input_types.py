"""Consolidate InputModels into semantically meaningful types."""

from typing import Union

from ..input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    OT2InputModel,
    OT3InputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)

Modules = Union[
    HeaterShakerModuleInputModel,
    ThermocyclerModuleInputModel,
    TemperatureModuleInputModel,
    MagneticModuleInputModel,
]
Robots = Union[OT2InputModel, OT3InputModel]
Containers = Union[Robots, Modules]
