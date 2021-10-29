from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from consts import (
    PRODUCTION_MODE_NAME,
    DEVELOPMENT_MODE_NAME
)

class EmulationSubCommands(str, Enum):
    PROD_MODE = PRODUCTION_MODE_NAME
    DEV_MODE = DEVELOPMENT_MODE_NAME


class CommonEmulationOptions(str, Enum):
    DETACHED = "detached"


class ProductionEmulationOptions(str, Enum):
    OT3_FIRMWARE_SHA = 'ot3-firmware-repo-sha'
    MODULES_SHA = 'opentrons-modules-repo-sha'
    MONOREPO_SHA = 'opentrons-repo-sha'


class DevelopmentEmulationOptions(str, Enum):
    MODULES_PATH = "--opentrons-modules-repo-path"
    OT3_FIRMWARE_PATH = "--ot3-firmware-repo-path"
    OPENTRONS_REPO = "--opentrons-repo-path"


class InvalidModeError(ValueError):
    pass


@dataclass
class ProdEmulationCreator:
    detached: bool = False
    ot3_firmware_sha: str = ''
    modules_sha: str = ''
    opentrons_sha: str = ''

    @classmethod
    def from_cli_input(cls, args) -> ProdEmulationCreator:
        return cls(
            detached=args.detached,
            ot3_firmware_sha=args.ot3_firmware_repo_sha,
            modules_sha=args.opentrons_modules_repo_sha,
            opentrons_sha=args.opentrons_repo_sha
        )


@dataclass
class DevEmulationCreator:
    detached: bool = False
    ot3_firmware_path: str = ''
    modules_path: str = ''
    opentrons_path: str = ''

    @classmethod
    def from_cli_input(cls, args) -> DevEmulationCreator:
        return cls(
            detached=args.detached,
            ot3_firmware_path=args.ot3_firmware_repo_path,
            modules_path=args.opentrons_modules_repo_path,
            opentrons_path=args.opentrons_repo_path
        )
