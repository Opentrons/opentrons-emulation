from __future__ import annotations

import subprocess
from dataclasses import dataclass
from enum import Enum
from consts import (
    PRODUCTION_MODE_NAME,
    DEVELOPMENT_MODE_NAME,
    ROOT_DIR
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

    OT3_FIRMWARE_DOCKER_ENV_VAR_NAME = "OT3_FIRMWARE_DIRECTORY"
    MODULES_DOCKER_ENV_VAR_NAME = "OPENTRONS_MODULES_DIRECTORY"
    OPENTRONS_DOCKER_ENV_VAR_NAME = 'OPENTRONS_DIRECTORY'

    detached: bool = False
    ot3_firmware_path: str = ''
    modules_path: str = ''
    opentrons_path: str = ''

    @classmethod
    def from_cli_input(cls, args) -> None:
        obj = cls(
            detached=args.detached,
            ot3_firmware_path=args.ot3_firmware_repo_path,
            modules_path=args.opentrons_modules_repo_path,
            opentrons_path=args.opentrons_repo_path
        )
        obj.clean()
        obj.build()
        obj.run()

    def build(self):
        cmd = (
            "COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 "
            f"{self.OT3_FIRMWARE_DOCKER_ENV_VAR_NAME}={self.ot3_firmware_path} "
            f"{self.MODULES_DOCKER_ENV_VAR_NAME}={self.modules_path} "
            f"{self.OPENTRONS_DOCKER_ENV_VAR_NAME}={self.opentrons_path} "
            "docker-compose --verbose -f docker-compose-dev.yaml build"
        )
        subprocess.run(cmd, cwd=ROOT_DIR, shell=True).check_returncode()

    def clean(self):
        cmd = "docker-compose kill && docker-compose rm -f"
        subprocess.run(cmd, cwd=ROOT_DIR, shell=True).check_returncode()

    def run(self):
        cmd = (
            f"{self.OT3_FIRMWARE_DOCKER_ENV_VAR_NAME}={self.ot3_firmware_path} "
            f"{self.MODULES_DOCKER_ENV_VAR_NAME}={self.modules_path} "
            f"{self.OPENTRONS_DOCKER_ENV_VAR_NAME}={self.opentrons_path} "
            "docker-compose up "
        )

        if self.detached:
            cmd += "-d"

        subprocess.run(cmd, cwd=ROOT_DIR, shell=True).check_returncode()