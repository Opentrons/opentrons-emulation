from __future__ import annotations

import argparse
import os
from typing import List, Dict

import pydantic
from dataclasses import dataclass
from enum import Enum

from emulation_system.commands.command import CommandList, Command
from emulation_system.settings import ROOT_DIR
from emulation_system.commands.abstract_command_creator import (
    AbstractCommandCreator,
)
from emulation_system.settings_models import ConfigurationSettings, SharedFolder


class VirtualMachineSubCommands(str, Enum):
    """Sub-command available to virtual-machine cli command"""

    CREATE = "create"
    SHELL = "shell"
    REMOVE = "remove"


class VirtualMachineSubCommandOptions(str, Enum):
    """Mode for virtual-machine subcommand
    Either prod or dev"""

    MODE = "mode"


class InvalidCommandError(ValueError):
    """Error thrown if virtual-machine sub-command is not
    create, shell, or remove"""

    pass


class VirtualMachineConfig(pydantic.BaseModel):
    """Model for json parameter file that needs to be specified to Vagrant"""

    VM_MEMORY: int
    VM_CPUS: int
    PRODUCTION_VM_NAME: str
    DEVELOPMENT_VM_NAME: str
    OPENTRONS_MODULES_PATH: str
    OT3_FIRMWARE_PATH: str
    OPENTRONS_PATH: str
    NUM_SOCKET_CAN_NETWORKS: str
    SHARED_FOLDERS: List[SharedFolder]


@dataclass
class VirtualMachineCommandCreator(AbstractCommandCreator):
    """Class to build vagrant commands for creating a Virtual Machine
    Supports create, shell, remove"""

    VAGRANT_RESOURCES_LOCATION = os.path.join(
        ROOT_DIR, "emulation_system/resources/vagrant"
    )
    SETTINGS_FILE_LOCATION = os.path.join(
        ROOT_DIR, "emulation_system/resources/vagrant/settings.json"
    )
    CREATE_COMMAND_NAME = "Create"
    SHELL_COMMAND_NAME = "Shell"
    REMOVE_COMMAND_NAME = "Remove"

    command: str
    mode: str
    dry_run: bool = False

    def __post_init__(self) -> None:
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
        cls, args: argparse.Namespace, settings: ConfigurationSettings
    ) -> VirtualMachineCommandCreator:
        """Construct VirtualMachineCommandCreator from CLI input
        Also creates settings.json file to pass with vagrant commands"""
        cls._create_json_settings_file(settings)
        return cls(command=args.vm_command, mode=args.mode, dry_run=args.dry_run)

    @classmethod
    def _create_json_settings_file(cls, settings_object: ConfigurationSettings) -> None:
        """Build settings.json file which defines all parameters to be supplied
        to vagrant commands"""
        vm_settings = settings_object.virtual_machine_settings
        default_folder_paths = settings_object.global_settings.default_folder_paths

        json_output = VirtualMachineConfig(
            VM_MEMORY=vm_settings.vm_memory,
            VM_CPUS=vm_settings.vm_cpus,
            PRODUCTION_VM_NAME=vm_settings.prod_vm_name,
            DEVELOPMENT_VM_NAME=vm_settings.dev_vm_name,
            OPENTRONS_MODULES_PATH=default_folder_paths.modules,
            OT3_FIRMWARE_PATH=default_folder_paths.ot3_firmware,
            OPENTRONS_PATH=default_folder_paths.opentrons,
            NUM_SOCKET_CAN_NETWORKS=str(vm_settings.num_socket_can_networks),
            SHARED_FOLDERS=vm_settings.shared_folders
        ).json(indent=4)

        settings_file = open(cls.SETTINGS_FILE_LOCATION, "w")
        settings_file.write(json_output)
        settings_file.close()

    def get_commands(self) -> CommandList:
        """Returns list of commands to run with vagrant"""
        return CommandList(
            command_list=[self.command_mapping[self.command]()], dry_run=self.dry_run
        )

    def create(self) -> Command:
        """Command to build and start a Virtual Machine"""
        return Command(
            command_name=self.CREATE_COMMAND_NAME,
            command=f"vagrant up {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION,
        )

    def shell(self) -> Command:
        """Command to open a shell to a VirtualMachine"""
        return Command(
            command_name=self.SHELL_COMMAND_NAME,
            command=f"vagrant ssh {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION,
            shell=True
        )

    def remove(self) -> Command:
        """Command to remove Virtual Machine"""
        return Command(
            command_name=self.REMOVE_COMMAND_NAME,
            command=f"vagrant destroy --force {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION,
        )
