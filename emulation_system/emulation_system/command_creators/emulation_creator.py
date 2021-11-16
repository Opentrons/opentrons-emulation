from __future__ import annotations

import abc
import argparse
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict

from emulation_system.settings import (
    PRODUCTION_MODE_NAME,
    DEVELOPMENT_MODE_NAME,
    LATEST_KEYWORD,
    ROOT_DIR,
)
from emulation_system.command_creators.command import CommandList, Command
from emulation_system.command_creators.abstract_command_creator import (
    AbstractCommandCreator,
)
from emulation_system.settings_models import (
    ConfigurationSettings,
    SourceDownloadLocations,
)


class CommonEmulationOptions(str, Enum):
    """Options shared by all sub-commands"""

    DETACHED = "--detached"


class EmulationSubCommands(str, Enum):
    """Sub-Commands available to the `emulation` command"""

    PROD_MODE = PRODUCTION_MODE_NAME
    DEV_MODE = DEVELOPMENT_MODE_NAME


class ProductionEmulationOptions(str, Enum):
    """Options specific to `prod` sub-command"""

    OT3_FIRMWARE_SHA = "--ot3-firmware-repo-sha"
    MODULES_SHA = "--opentrons-modules-repo-sha"
    MONOREPO_SHA = "--opentrons-repo-sha"


class DevelopmentEmulationOptions(str, Enum):
    """Options specfic to `dev` sub-command"""

    MODULES_PATH = "--opentrons-modules-repo-path"
    OT3_FIRMWARE_PATH = "--ot3-firmware-repo-path"
    OPENTRONS_REPO = "--opentrons-repo-path"


class InvalidModeError(ValueError):
    """Thrown when an invalid emulation mode is provided.
    (Not `prod` or `dev`)"""

    pass


class AbstractEmulationCreator(AbstractCommandCreator):
    """Things common to both EmulationCreator classes"""

    BUILD_COMMAND_NAME = "Build Emulation"
    KILL_COMMAND_NAME = "Kill Emulation"
    REMOVE_COMMAND_NAME = "Remove Emulation"
    RUN_COMMAND_NAME = "Run Emulation"

    DOCKER_RESOURCES_LOCATION = os.path.join(
        ROOT_DIR, "emulation_system/resources/docker"
    )

    DOCKER_BUILD_ENV_VARS = {"COMPOSE_DOCKER_CLI_BUILD": "1", "DOCKER_BUILDKIT": "1"}

    @property
    @abc.abstractmethod
    def compose_file_name(self):
        ...

    @abc.abstractmethod
    def build(self):
        ...

    @abc.abstractmethod
    def run(self):
        ...

    @property
    @abc.abstractmethod
    def dry_run(self):
        ...

    def kill(self) -> Command:
        """Kill and remove any existing dev containers"""
        return Command(
            command_name=self.KILL_COMMAND_NAME,
            command=f"docker-compose -f {self.compose_file_name} kill",
            cwd=self.DOCKER_RESOURCES_LOCATION,
        )

    def remove(self) -> Command:
        """Kill and remove any existing dev containers"""
        return Command(
            command_name=self.REMOVE_COMMAND_NAME,
            command=f"docker-compose -f {self.compose_file_name} rm -f",
            cwd=self.DOCKER_RESOURCES_LOCATION,
        )

    def _get_commands(self) -> CommandList:
        return CommandList(
            command_list=[
                self.kill(),
                self.remove(),
                self.build(),
                self.run(),
            ],
            dry_run=self.dry_run,
        )


@dataclass
class ProdEmulationCreator(AbstractEmulationCreator):
    """Class to build docker commands for creating a Production Emulator
    Supports `build`, `clean`, and `run` commands"""

    detached: bool = False
    ot3_firmware_download_location: str = ""
    modules_download_location: str = ""
    opentrons_download_location: str = ""
    dry_run: bool = False

    # Pulled from Dockerfile in root of repo
    OT3_FIRMWARE_DOCKER_BUILD_ARG_NAME = "FIRMWARE_SOURCE_DOWNLOAD_LOCATION"
    MODULES_DOCKER_BUILD_ARG_NAME = "MODULE_SOURCE_DOWNLOAD_LOCATION"
    OPENTRONS_DOCKER_BUILD_ARG_NAME = "OPENTRONS_SOURCE_DOWNLOAD_LOCATION"

    @property
    def compose_file_name(self) -> str:
        """Compose file name to use"""
        return "docker-compose.yaml"

    @classmethod
    def from_cli_input(
        cls, args: argparse.Namespace, settings: ConfigurationSettings
    ) -> ProdEmulationCreator:
        """Factory method to convert CLI input into a ProdEmulatorCreator object"""
        download_locations = settings.emulation_settings.source_download_locations
        return cls(
            detached=args.detached,
            ot3_firmware_download_location=cls._parse_download_location(
                "ot3_firmware", args.ot3_firmware_repo_sha, download_locations
            ),
            modules_download_location=cls._parse_download_location(
                "modules", args.opentrons_modules_repo_sha, download_locations
            ),
            opentrons_download_location=cls._parse_download_location(
                "opentrons", args.opentrons_repo_sha, download_locations
            ),
            dry_run=args.dry_run,
        )

    @staticmethod
    def _parse_download_location(
        key: str, location: str, download_locations: SourceDownloadLocations
    ) -> str:
        """Parse download location from passed `location` parameter into a
        downloadable source code zip file"""
        if location == LATEST_KEYWORD:
            download_location = download_locations.heads.__getattribute__(key)
        else:
            download_location = download_locations.commits.__getattribute__(
                key
            ).replace("{{commit-sha}}", location)
        return download_location

    def build(self) -> Command:
        """Construct a docker-compose build command"""
        cmd = (
            f"docker-compose -f {self.compose_file_name} build "
            f"--build-arg {self.OT3_FIRMWARE_DOCKER_BUILD_ARG_NAME}="
            f"{self.ot3_firmware_download_location} "
            f"--build-arg {self.MODULES_DOCKER_BUILD_ARG_NAME}="
            f"{self.modules_download_location} "
            f"--build-arg {self.OPENTRONS_DOCKER_BUILD_ARG_NAME}="
            f"{self.opentrons_download_location} "
        )

        return Command(
            command_name=self.BUILD_COMMAND_NAME,
            command=cmd,
            cwd=self.DOCKER_RESOURCES_LOCATION,
            env=self.DOCKER_BUILD_ENV_VARS,
        )

    def run(self) -> Command:
        """Construct a docker-compose up command"""
        cmd = f"docker-compose -f {self.compose_file_name} up"

        if self.detached:
            cmd += " -d"

        return Command(
            command_name=self.RUN_COMMAND_NAME,
            command=cmd,
            cwd=self.DOCKER_RESOURCES_LOCATION,
        )

    def get_commands(self) -> CommandList:
        """Get a list of commands to create emulation"""
        return self._get_commands()


@dataclass
class DevEmulationCreator(AbstractEmulationCreator):
    """Command creator for `dev` sub-command of `emulation` command.
    Supports `build`, `clean`, and `run` commands"""

    OT3_FIRMWARE_DOCKER_ENV_VAR_NAME = "OT3_FIRMWARE_DIRECTORY"
    MODULES_DOCKER_ENV_VAR_NAME = "OPENTRONS_MODULES_DIRECTORY"
    OPENTRONS_DOCKER_ENV_VAR_NAME = "OPENTRONS_DIRECTORY"

    detached: bool = False
    ot3_firmware_path: str = ""
    modules_path: str = ""
    opentrons_path: str = ""
    dry_run: bool = False

    def _get_run_env_vars(self) -> Dict[str, str]:
        return {
            self.OT3_FIRMWARE_DOCKER_ENV_VAR_NAME: self.ot3_firmware_path,
            self.MODULES_DOCKER_ENV_VAR_NAME: self.modules_path,
            self.OPENTRONS_DOCKER_ENV_VAR_NAME: self.opentrons_path,
        }

    def _get_build_env_vars(self):
        default_vars_copy = self.DOCKER_BUILD_ENV_VARS.copy()
        default_vars_copy.update(self._get_run_env_vars())
        return default_vars_copy

    @property
    def compose_file_name(self) -> str:
        """Compose file name to use"""
        return "docker-compose-dev.yaml"

    @classmethod
    def from_cli_input(
        cls, args: argparse.Namespace, settings: ConfigurationSettings
    ) -> DevEmulationCreator:
        """Factory method to convert CLI input into a DevEmulatorCreator object"""
        return cls(
            detached=args.detached,
            ot3_firmware_path=args.ot3_firmware_repo_path,
            modules_path=args.opentrons_modules_repo_path,
            opentrons_path=args.opentrons_repo_path,
            dry_run=args.dry_run,
        )

    def build(self) -> Command:
        """Construct a docker-compose build command"""
        # Need to specify env vars to satisfy docker-compose file even though nothing
        # is done with the env vars

        return Command(
            command_name=self.BUILD_COMMAND_NAME,
            command=f"docker-compose -f {self.compose_file_name} build",
            cwd=self.DOCKER_RESOURCES_LOCATION,
            env=self._get_build_env_vars(),
        )

    def run(self) -> Command:
        """Construct a docker-compose up command"""
        cmd = f"docker-compose -f {self.compose_file_name} up"

        if self.detached:
            cmd += " -d"

        return Command(
            command_name=self.RUN_COMMAND_NAME,
            command=cmd,
            cwd=self.DOCKER_RESOURCES_LOCATION,
            env=self._get_run_env_vars(),
        )

    def get_commands(self) -> CommandList:
        """Get a list of commands to create emulation"""
        return self._get_commands()
