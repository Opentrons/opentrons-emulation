"""Functions for usage with HardwareModel objects."""
from typing import TypeGuard

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    SourceType,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    ModuleInputModel,
    OT2InputModel,
    OT3InputModel,
    RobotInputModel,
)
from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
)


def is_robot(hardware: HardwareModel) -> TypeGuard[RobotInputModel]:
    """Whether hardware is a robot."""
    return issubclass(hardware.__class__, RobotInputModel)


def is_module(hardware: HardwareModel) -> TypeGuard[ModuleInputModel]:
    """Whether hardware is a module."""
    return issubclass(hardware.__class__, ModuleInputModel)


def is_ot2(hardware: HardwareModel) -> TypeGuard[OT2InputModel]:
    """Whether hardware is an OT-2."""
    return isinstance(hardware, OT2InputModel)


def is_ot3(hardware: HardwareModel) -> TypeGuard[OT3InputModel]:
    """Whether hardware is an OT-3"""
    return isinstance(hardware, OT3InputModel)


def is_remote_robot(hardware: HardwareModel) -> TypeGuard[RobotInputModel]:
    """Whether hardware is a remote robot."""
    return (
        is_robot(hardware)
        and hasattr(hardware, "robot_server_source_type")
        and getattr(hardware, "robot_server_source_type") == SourceType.REMOTE
    )


def is_remote_module(hardware: HardwareModel) -> TypeGuard[ModuleInputModel]:
    """Whether hardware is a remote module."""
    return (
        is_module(hardware)
        and hasattr(hardware, "source_type")
        and getattr(hardware, "source_type") == SourceType.REMOTE
    )


def is_hardware_emulation_level(hardware: HardwareModel) -> bool:
    """Whether hardware is hardware emulation level."""
    return hardware.emulation_level == EmulationLevels.HARDWARE
