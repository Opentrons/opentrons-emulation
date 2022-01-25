"""Builds commands for creating virtual machines."""

from __future__ import annotations

import argparse
import os
from typing import List

from pydantic import BaseModel, parse_obj_as
from dataclasses import dataclass
from enum import Enum

from emulation_system.commands.sub_process_command import (
    SubProcessCommandList,
    SubProcessCommand,
)
from emulation_system.consts import ROOT_DIR
from emulation_system.commands.abstract_command import (
    AbstractCommand,
)
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
class VirtualMachineCommand(AbstractCommand):
    """Class to build vagrant commands for creating a Virtual Machine.

    Supports create, shell, remove.
    """

    VAGRANT_RESOURCES_LOCATION = os.path.join(
        ROOT_DIR, "emulation_system/resources/vagrant"
    )
    SETTINGS_FILE_LOCATION = os.path.join(
        ROOT_DIR, "emulation_system/resources/vagrant/settings.json"
    )
    CREATE_COMMAND_NAME = "Create"
    SHELL_COMMAND_NAME = "Shell"
    REMOVE_COMMAND_NAME = "Remove"

    LOCAL_EMULATION_FOLDER_LOCATION = os.path.normpath(os.path.join("..", ROOT_DIR))
    VAGRANT_HOME_LOCATION = "/home/vagrant"

    command: str
    mode: str
    dry_run: bool = False

    def __post_init__(self) -> None:
        """Build command mapping and validate that correct command was passed."""
        self.command_mapping = {
            VirtualMachineSubCommands.CREATE.value: self.create,
            VirtualMachineSubCommands.SHELL.value: self.shell,
            VirtualMachineSubCommands.REMOVE.value: self.remove,
        }
        if self.command not in self.command_mapping.keys():
            command_string = ", ".join(self.command_mapping.keys())
            raise InvalidCommandError(
                f'"command" must be one of the following values: {command_string}'
            )

    @classmethod
    def from_cli_input(
        cls, args: argparse.Namespace, settings: OpentronsEmulationConfiguration
    ) -> SubProcessCommandList:
        """Construct VirtualMachineCommand from CLI input.

        Also creates settings.json file to pass with vagrant commands.
        """
        cls._create_json_settings_file(settings)
        return cls(
            command=args.vm_command, mode=args.mode, dry_run=args.dry_run
        ).get_commands()

    @classmethod
    def _add_source_code_folder(cls, host_path: str) -> SharedFolder:
        """If host path was defined, add it to list of folders to create on VM."""
        vm_path = os.path.join(cls.VAGRANT_HOME_LOCATION, os.path.basename(host_path))
        return parse_obj_as(SharedFolder, {"host-path": host_path, "vm-path": vm_path})

    @classmethod
    def _create_json_settings_file(
        cls, settings_object: OpentronsEmulationConfiguration
    ) -> None:
        """Build settings file for vagrant commands."""
        vm_settings = settings_object.virtual_machine_settings
        default_folder_paths = settings_object.global_settings.default_folder_paths
        folders = [
            default_folder_paths.opentrons,
            default_folder_paths.ot3_firmware,
            default_folder_paths.modules,
            cls.LOCAL_EMULATION_FOLDER_LOCATION,
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
                cls._add_source_code_folder(folder_path)
                for folder_path in folders
                if folder_path is not None
            ],
        ).json(indent=4)

        settings_file = open(cls.SETTINGS_FILE_LOCATION, "w")
        settings_file.write(json_output)
        settings_file.close()

    def get_commands(self) -> SubProcessCommandList:
        """Returns list of commands to run with vagrant."""
        return SubProcessCommandList(
            command_list=[self.command_mapping[self.command]()], dry_run=self.dry_run
        )

    def create(self) -> SubProcessCommand:
        """SubProcessCommand to build and start a Virtual Machine."""  # noqa: D403
        return SubProcessCommand(
            command_name=self.CREATE_COMMAND_NAME,
            command=f"vagrant up {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION,
        )

    def shell(self) -> SubProcessCommand:
        """SubProcessCommand to open a shell to a VirtualMachine."""  # noqa: D403
        return SubProcessCommand(
            command_name=self.SHELL_COMMAND_NAME,
            command=f"vagrant ssh {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION,
            shell=True,
        )

    def remove(self) -> SubProcessCommand:
        """SubProcessCommand to remove Virtual Machine."""  # noqa: D403
        return SubProcessCommand(
            command_name=self.REMOVE_COMMAND_NAME,
            command=f"vagrant destroy --force {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION,
        )
