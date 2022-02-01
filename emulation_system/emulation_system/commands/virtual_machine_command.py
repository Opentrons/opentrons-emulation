"""Builds commands for creating virtual machines."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from enum import Enum
from typing import List

from pydantic import (
    BaseModel,
    parse_obj_as,
)

from emulation_system.consts import ROOT_DIR
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
    SharedFolder,
)


class VirtualMachineSubCommands(str, Enum):
    """Sub-command available to virtual-machine cli command."""

    CREATE = "create"
    SHELL = "shell"
    REMOVE = "remove"


class VirtualMachineSubCommandOptions(str, Enum):
    """Mode for virtual-machine subcommand. Either prod or dev."""

    MODE = "mode"


class InvalidCommandError(ValueError):
    """Error thrown if virtual-machine sub-command is not create, shell, or remove."""

    pass


class VirtualMachineConfig(BaseModel):
    """Model for json parameter file that needs to be specified to Vagrant."""

    VM_MEMORY: int
    VM_CPUS: int
    PRODUCTION_VM_NAME: str
    DEVELOPMENT_VM_NAME: str
    NUM_SOCKET_CAN_NETWORKS: str
    SHARED_FOLDERS: List[SharedFolder]


@dataclass
class VirtualMachineCommand:
    LOCAL_EMULATION_FOLDER_LOCATION = os.path.normpath(os.path.join("..", ROOT_DIR))
    VAGRANT_HOME_LOCATION = "/home/vagrant"
    SETTINGS_FILE_LOCATION = os.path.join(
        ROOT_DIR, "vagrant", "settings.json"
    )

    settings: OpentronsEmulationConfiguration

    @classmethod
    def from_cli_input(
        cls, args: argparse.Namespace, settings: OpentronsEmulationConfiguration
    ) -> VirtualMachineCommand:
        """Construct EmulationSystemCommand from CLI input."""
        return cls(settings=settings)

    def _add_source_code_folder(self, host_path: str) -> SharedFolder:
        """If host path was defined, add it to list of folders to create on VM."""
        vm_path = os.path.join(self.VAGRANT_HOME_LOCATION, os.path.basename(host_path))
        return parse_obj_as(SharedFolder, {"host-path": host_path, "vm-path": vm_path})

    def execute(self) -> None:
        """Build settings file for vagrant commands."""
        vm_settings = self.settings.virtual_machine_settings
        default_folder_paths = self.settings.global_settings.default_folder_paths
        folders = [
            default_folder_paths.opentrons,
            default_folder_paths.ot3_firmware,
            default_folder_paths.modules,
            self.LOCAL_EMULATION_FOLDER_LOCATION,
        ]

        if vm_settings.shared_folders is not None:
            folders += vm_settings.shared_folders

        json_output = VirtualMachineConfig(
            VM_MEMORY=vm_settings.vm_memory,
            VM_CPUS=vm_settings.vm_cpus,
            PRODUCTION_VM_NAME=vm_settings.prod_vm_name,
            DEVELOPMENT_VM_NAME=vm_settings.dev_vm_name,
            NUM_SOCKET_CAN_NETWORKS=str(vm_settings.num_socket_can_networks),
            SHARED_FOLDERS=[
                self._add_source_code_folder(folder_path)
                for folder_path in folders
                if folder_path is not None
            ],
        ).json()

        settings_file = open(self.SETTINGS_FILE_LOCATION, "w")
        settings_file.write(json_output)
        settings_file.close()
