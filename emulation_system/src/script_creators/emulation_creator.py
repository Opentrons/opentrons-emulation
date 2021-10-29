from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class EmulationOptions(str, Enum):
    MODE = "mode"
    DETACHED = "detached"
    OT3_FIRMWARE_SHA = 'ot3-firmware-sha'
    MODULES_SHA = 'modules-sha'


class InvalidModeError(ValueError):
    pass

@dataclass
class EmulationCreator:
    PROD_MODE = "prod"
    DEV_MODE = "dev"

    mode: str
    detached: bool = False
    ot3_firmware_sha: str = ''
    modules_sha: str = ''

    @classmethod
    def from_cli_input(cls, args) -> EmulationCreator:
        return cls(
            mode=args.mode,
            detached=args.detached,
            ot3_firmware_sha=args.ot3_firmware_sha,
            modules_sha=args.modules_sha
        )

    def __post_init__(self):
        if self.mode not in [self.PROD_MODE, self.DEV_MODE]:
            raise InvalidModeError(
                f"\"mode\" must either be {self.PROD_MODE} or {self.DEV_MODE}"
            )
