from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from settings import PRODUCTION_MODE_NAME, DEVELOPMENT_MODE_NAME
from command_creators.command import CommandList, Command
from command_creators.command_creator import CommandCreator


class EmulationSubCommands(str, Enum):
    """Sub-Commands available to the `emulation` command"""
    PROD_MODE = PRODUCTION_MODE_NAME
    DEV_MODE = DEVELOPMENT_MODE_NAME


class CommonEmulationOptions(str, Enum):
    """Options shared by all sub-commands"""
    DETACHED = "detached"


class ProductionEmulationOptions(str, Enum):
    """Options specific to `prod` sub-command"""
    OT3_FIRMWARE_SHA = 'ot3-firmware-repo-sha'
    MODULES_SHA = 'opentrons-modules-repo-sha'
    MONOREPO_SHA = 'opentrons-repo-sha'


class DevelopmentEmulationOptions(str, Enum):
    """Options specfic to `dev` sub-command"""
    MODULES_PATH = "--opentrons-modules-repo-path"
    OT3_FIRMWARE_PATH = "--ot3-firmware-repo-path"
    OPENTRONS_REPO = "--opentrons-repo-path"


class InvalidModeError(ValueError):
    """Thrown when an invalid emulation mode is provided.
    (Not `prod` or `dev`)"""
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
class DevEmulationCreator(CommandCreator):
    """Command creator for `dev` sub-command of `emulation` command.
    Supports `build`, `clean`, and `run` commands"""

    OT3_FIRMWARE_DOCKER_ENV_VAR_NAME = "OT3_FIRMWARE_DIRECTORY"
    MODULES_DOCKER_ENV_VAR_NAME = "OPENTRONS_MODULES_DIRECTORY"
    OPENTRONS_DOCKER_ENV_VAR_NAME = 'OPENTRONS_DIRECTORY'

    BUILD_COMMAND_NAME = "Build Emulation"
    CLEAN_COMMAND_NAME = "Clean Emulation"
    RUN_COMMAND_NAME = "Run Emulation"

    detached: bool = False
    ot3_firmware_path: str = ''
    modules_path: str = ''
    opentrons_path: str = ''

    @classmethod
    def from_cli_input(cls, args) -> CommandList:
        """Parse input from CLI into a runnable command"""
        return cls(
            detached=args.detached,
            ot3_firmware_path=args.ot3_firmware_repo_path,
            modules_path=args.opentrons_modules_repo_path,
            opentrons_path=args.opentrons_repo_path
        )


    def build(self) -> Command:
        """Build dev images with Docker Buildkit.
        Use inline env vars for source code folders
        """
        cmd = (
            "COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 "
            f"{self.OT3_FIRMWARE_DOCKER_ENV_VAR_NAME}={self.ot3_firmware_path} "
            f"{self.MODULES_DOCKER_ENV_VAR_NAME}={self.modules_path} "
            f"{self.OPENTRONS_DOCKER_ENV_VAR_NAME}={self.opentrons_path} "
            "docker-compose --verbose -f docker-compose-dev.yaml build"
        )
        return Command(self.BUILD_COMMAND_NAME, cmd)

    def clean(self):
        """Kill and remove any existing dev containers"""
        cmd = "docker-compose kill && docker-compose rm -f"
        return Command(self.CLEAN_COMMAND_NAME, cmd)

    def run(self):
        """Start containers"""
        cmd = (
            f"{self.OT3_FIRMWARE_DOCKER_ENV_VAR_NAME}={self.ot3_firmware_path} "
            f"{self.MODULES_DOCKER_ENV_VAR_NAME}={self.modules_path} "
            f"{self.OPENTRONS_DOCKER_ENV_VAR_NAME}={self.opentrons_path} "
            "docker-compose up "
        )

        if self.detached:
            cmd += "-d"

        return Command(self.RUN_COMMAND_NAME, cmd)

    def get_commands(self) -> CommandList:
        return CommandList(
            [
                self.clean(),
                self.build(),
                self.run(),
            ]
        )
