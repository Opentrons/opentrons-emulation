"""Functions for usage with HardwareModel objects."""
from typing import TypeGuard

from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    ModuleInputModel,
    OT2InputModel,
    OT3InputModel,
    RobotInputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)


def is_robot(obj: object) -> TypeGuard[RobotInputModel]:
    """Whether hardware is a robot."""
    return issubclass(obj.__class__, RobotInputModel)


def is_module(obj: object) -> TypeGuard[ModuleInputModel]:
    """Whether hardware is a module."""
    return issubclass(obj.__class__, ModuleInputModel)


def is_ot2(obj: object) -> TypeGuard[OT2InputModel]:
    """Whether hardware is an OT-2."""
    return isinstance(obj, OT2InputModel)


def is_ot3(obj: object) -> TypeGuard[OT3InputModel]:
    """Whether hardware is an OT-3"""
    return isinstance(obj, OT3InputModel)


def is_heater_shaker_module(obj: object) -> TypeGuard[HeaterShakerModuleInputModel]:
    """Whether hardware is a heater-shaker module."""
    return isinstance(obj, HeaterShakerModuleInputModel)


def is_magnetic_module(obj: object) -> TypeGuard[MagneticModuleInputModel]:
    """Whether hardware is a magnetic module."""
    return isinstance(obj, MagneticModuleInputModel)


def is_temperature_module(
    obj: object,
) -> TypeGuard[TemperatureModuleInputModel]:
    """Whether hardware is a temperature module."""
    return isinstance(obj, TemperatureModuleInputModel)


def is_thermocycler_module(
    obj: object,
) -> TypeGuard[ThermocyclerModuleInputModel]:
    """Whether hardware is a thermocycler module."""
    return isinstance(obj, ThermocyclerModuleInputModel)
