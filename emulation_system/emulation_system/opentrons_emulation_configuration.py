"""Models for configuration_settings.json file."""

from __future__ import annotations

import json
import os

from pydantic import BaseModel, Field, parse_obj_as

from emulation_system.compose_file_creator.errors import RepoDoesNotExistError
from emulation_system.compose_file_creator.settings.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.consts import (
    CONFIGURATION_FILE_LOCATION_VAR_NAME,
    DEFAULT_CONFIGURATION_FILE_PATH,
)


class ConfigurationFileNotFoundError(FileNotFoundError):
    """Error thrown when config file is not found."""

    pass


class Heads(BaseModel):
    """Where to download the head of the repos from."""

    opentrons: str
    ot3_firmware: str = Field(..., alias="ot3-firmware")
    modules: str


class Commits(BaseModel):
    """Format string for where to download a specific commit sha from."""

    opentrons: str
    ot3_firmware: str = Field(..., alias="ot3-firmware")
    modules: str


class SourceDownloadLocations(BaseModel):
    """Model representing where to download source code from."""

    heads: Heads
    commits: Commits


class EmulationSettings(BaseModel):
    """All settings related to `em` command."""

    source_download_locations: SourceDownloadLocations = Field(
        ..., alias="source-download-locations"
    )


class OpentronsEmulationConfiguration(BaseModel):
    """Model representing entire configuration file."""

    emulation_settings: EmulationSettings = Field(..., alias="emulation-settings")

    @classmethod
    def from_file_path(cls, json_file_path: str) -> OpentronsEmulationConfiguration:
        """Parse file in OpentronsEmulationConfiguration object."""
        try:
            file = open(json_file_path, "r")
        except FileNotFoundError:
            raise ConfigurationFileNotFoundError(
                f"\nError loading configuration file.\n"
                f"Configuration file not found at: {json_file_path}\n"
                f"Please create a JSON configuration file"
            )

        return parse_obj_as(cls, json.load(file))

    def get_repo_commit(self, repo: OpentronsRepository) -> str:
        """Helper method to get repo commit string."""
        lookup = {
            OpentronsRepository.OPENTRONS: self.emulation_settings.source_download_locations.commits.opentrons,
            OpentronsRepository.OT3_FIRMWARE: self.emulation_settings.source_download_locations.commits.ot3_firmware,
            OpentronsRepository.OPENTRONS_MODULES: self.emulation_settings.source_download_locations.commits.modules,
        }

        try:
            commit = lookup[repo]
        except KeyError:
            raise RepoDoesNotExistError(repo.value)

        return commit

    def get_repo_head(self, repo: OpentronsRepository) -> str:
        """Helper method to get repo head string."""
        lookup = {
            OpentronsRepository.OPENTRONS: self.emulation_settings.source_download_locations.heads.opentrons,
            OpentronsRepository.OT3_FIRMWARE: self.emulation_settings.source_download_locations.heads.ot3_firmware,
            OpentronsRepository.OPENTRONS_MODULES: self.emulation_settings.source_download_locations.heads.modules,
        }

        try:
            head = lookup[repo]
        except KeyError:
            raise RepoDoesNotExistError(repo.value)

        return head


def load_opentrons_emulation_configuration_from_env() -> OpentronsEmulationConfiguration:
    """Helper function for loading OpentronsEmulationConfiguration object."""
    if CONFIGURATION_FILE_LOCATION_VAR_NAME in os.environ:
        file_path = os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME]
    else:
        file_path = DEFAULT_CONFIGURATION_FILE_PATH
    return OpentronsEmulationConfiguration.from_file_path(file_path)
