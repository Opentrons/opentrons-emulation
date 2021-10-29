from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict


class EmulationSubCommands(str, Enum):
    PROD_MODE = "prod"
    DEV_MODE = "dev"


class EmulationOptions(str, Enum):
    DETACHED = "detached"
    OT3_FIRMWARE_SHA = 'ot3-firmware-sha'
    MODULES_SHA = 'modules-sha'


class InvalidModeError(ValueError):
    pass


@dataclass
class ProdEmulationCreator:
    detached: bool = False
    ot3_firmware_sha: str = ''
    modules_sha: str = ''

    @classmethod
    def from_cli_input(cls, args) -> ProdEmulationCreator:
        return cls(
            detached=args.detached,
            ot3_firmware_sha=args.ot3_firmware_sha,
            modules_sha=args.modules_sha
        )


@dataclass
class DevEmulationCreator:
    detached: bool = False

    @classmethod
    def from_cli_input(cls, args) -> DevEmulationCreator:
        return cls(
            detached=args.detached
        )
