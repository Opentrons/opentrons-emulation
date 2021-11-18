from __future__ import annotations

import argparse
import os
from typing import List, Dict, Optional

from pydantic import BaseModel, parse_obj_as
from dataclasses import dataclass
from enum import Enum

from emulation_system.commands.command import CommandList, Command
from emulation_system.settings import ROOT_DIR
from emulation_system.commands.abstract_command_creator import (
    AbstractCommandCreator,
)
from emulation_system.settings_models import (
    ConfigurationSettings,
    SharedFolder,
    DefaultFolderPaths
)


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


class VirtualMachineConfig(BaseModel):
    """Model for json parameter file that needs to be specified to Vagrant"""

    VM_MEMORY: int
    VM_CPUS: int
    PRODUCTION_VM_NAME: str
    DEVELOPMENT_VM_NAME: str
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

    LOCAL_EMULATION_FOLDER_LOCATION = os.path.normpath(
        os.path.join(
            '..',
            ROOT_DIR,
        )
    )

    VAGRANT_HOME_LOCATION = '/home/vagrant'

    OPENTRONS_EMULATION_FOLDER_LOCATION = os.path.join(
        VAGRANT_HOME_LOCATION, 'opentrons-emulation'
    )
    OPENTRONS_MODULES_FOLDER_LOCATION = os.path.join(
        VAGRANT_HOME_LOCATION, 'opentrons-modules'
    )
    OPENTRONS_MONOREPO_FOLDER_LOCATION = os.path.join(
        VAGRANT_HOME_LOCATION, 'opentrons'
    )
    OT3_FIRMWARE_FOLDER_LOCATION = os.path.join(
        VAGRANT_HOME_LOCATION, 'ot3-firmware'
    )

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
    def _setup_default_folders(
            cls, default_folder_paths: DefaultFolderPaths
    ) -> List[SharedFolder]:
        """Sets up default folders: opentrons-emulation, opentrons, opentrons-modules,
        and ot3-firmware"""

        def add_source_code_folder(
                host_path: str, vm_path: str, folders: List[SharedFolder]
        ) -> None:
            """If host path was defined for source code, add it to list of
             shared folders to create on VM"""
            if host_path is not None:
                folders.append(
                    parse_obj_as(
                        SharedFolder,
                        {'host-path': host_path, 'vm-path': vm_path}
                    )
                )

        folders = []
        add_source_code_folder(
            default_folder_paths.modules,
            cls.OPENTRONS_MODULES_FOLDER_LOCATION,
            folders
        )
        add_source_code_folder(
            default_folder_paths.opentrons,
            cls.OPENTRONS_MONOREPO_FOLDER_LOCATION,
            folders
        )
        add_source_code_folder(
            default_folder_paths.ot3_firmware,
            cls.OT3_FIRMWARE_FOLDER_LOCATION,
            folders
        )
        add_source_code_folder(
            cls.LOCAL_EMULATION_FOLDER_LOCATION,
            cls.OPENTRONS_EMULATION_FOLDER_LOCATION,
            folders
        )
        return folders

    @classmethod
    def _create_json_settings_file(cls, settings_object: ConfigurationSettings) -> None:
        """Build settings.json file which defines all parameters to be supplied
        to vagrant commands"""
        vm_settings = settings_object.virtual_machine_settings
        default_folder_paths = settings_object.global_settings.default_folder_paths
        folders = cls._setup_default_folders(default_folder_paths)
        folders.extend(vm_settings.shared_folders)

        json_output = VirtualMachineConfig(
            VM_MEMORY=vm_settings.vm_memory,
            VM_CPUS=vm_settings.vm_cpus,
            PRODUCTION_VM_NAME=vm_settings.prod_vm_name,
            DEVELOPMENT_VM_NAME=vm_settings.dev_vm_name,
            NUM_SOCKET_CAN_NETWORKS=str(vm_settings.num_socket_can_networks),
            SHARED_FOLDERS=folders
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
