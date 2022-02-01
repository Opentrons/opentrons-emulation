"""Models for configuration_settings.json file."""

from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional

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


class DefaultFolderPaths(BaseModel):
    """Default folder paths to find repos at."""

    opentrons: Optional[str]
    ot3_firmware: Optional[str] = Field(alias="ot3-firmware")
    modules: Optional[str]


class GlobalSettings(BaseModel):
    """Settings that affect all sections in config file."""

    default_folder_paths: DefaultFolderPaths = Field(..., alias="default-folder-paths")


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


class SharedFolder(BaseModel):
    """Model for a shared folder. Will map host_path to vm_path."""

    host_path: str = Field(..., alias="host-path")
    vm_path: str = Field(..., alias="vm-path")


class VirtualMachineSettings(BaseModel):
    """All settings related to vm command."""

    dev_vm_name: str = Field(..., alias="dev-vm-name")
    prod_vm_name: str = Field(..., alias="prod-vm-name")
    vm_memory: int = Field(..., alias="vm-memory")
    vm_cpus: int = Field(..., alias="vm-cpus")
    num_socket_can_networks: int = Field(..., alias="num-socket-can-networks")
    shared_folders: List[str] = Field(alias="shared-folders", default=[])


class OpentronsEmulationConfiguration(BaseModel):
    """Model representing entire configuration file."""

    global_settings: GlobalSettings = Field(..., alias="global-settings")
    emulation_settings: EmulationSettings = Field(..., alias="emulation-settings")
    virtual_machine_settings: VirtualMachineSettings = Field(
        ..., alias="virtual-machine-settings"
    )
    aws_ecr_settings: Dict[str, Any] = Field(..., alias="aws-ecr-settings")

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
            OpentronsRepository.OPENTRONS: self.emulation_settings.source_download_locations.commits.opentrons,  # noqa: E501
            OpentronsRepository.OT3_FIRMWARE: self.emulation_settings.source_download_locations.commits.ot3_firmware,  # noqa: E501
            OpentronsRepository.OPENTRONS_MODULES: self.emulation_settings.source_download_locations.commits.modules,  # noqa: E501
        }

        try:
            commit = lookup[repo]
        except KeyError:
            raise RepoDoesNotExistError(repo.value)

        return commit

    def get_repo_head(self, repo: OpentronsRepository) -> str:
        """Helper method to get repo head string."""
        lookup = {
            OpentronsRepository.OPENTRONS: self.emulation_settings.source_download_locations.heads.opentrons,  # noqa: E501
            OpentronsRepository.OT3_FIRMWARE: self.emulation_settings.source_download_locations.heads.ot3_firmware,  # noqa: E501
            OpentronsRepository.OPENTRONS_MODULES: self.emulation_settings.source_download_locations.heads.modules,  # noqa: E501
        }

        try:
            head = lookup[repo]
        except KeyError:
            raise RepoDoesNotExistError(repo.value)

        return head


def load_opentrons_emulation_configuration_from_env() -> OpentronsEmulationConfiguration:  # noqa: E501
    """Helper function for loading OpentronsEmulationConfiguration object."""
    if CONFIGURATION_FILE_LOCATION_VAR_NAME in os.environ:
        file_path = os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME]
    else:
        file_path = DEFAULT_CONFIGURATION_FILE_PATH
    return OpentronsEmulationConfiguration.from_file_path(file_path)
