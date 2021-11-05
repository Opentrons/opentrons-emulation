from __future__ import annotations

import argparse
import os

import pydantic
from dataclasses import dataclass
from enum import Enum

from command_creators.command import CommandList, Command
from settings import ROOT_DIR
from command_creators.abstract_command_creator import AbstractCommandCreator
from settings_models import ConfigurationSettings


class VirtualMachineSubCommands(str, Enum):
    CREATE = "create"
    SHELL = "shell"
    REMOVE = "remove"


class VirtualMachineSubCommandOptions(str, Enum):
    MODE = "mode"


class InvalidCommandError(ValueError):
    pass


class VirtualMachineConfig(pydantic.BaseModel):
    VM_MEMORY: int
    VM_CPUS: int
    PRODUCTION_VM_NAME: str
    DEVELOPMENT_VM_NAME: str
    OPENTRONS_MODULES_PATH: str
    OT3_FIRMWARE_PATH: str
    OPENTRONS_PATH: str
    NUM_SOCKET_CAN_NETWORKS: str


@dataclass
class VirtualMachineCreator(AbstractCommandCreator):

    VAGRANT_RESOURCES_LOCATION = os.path.join(
        ROOT_DIR,
        "emulation_system/resources/vagrant"
    )
    SETTINGS_FILE_LOCATION = os.path.join(
        ROOT_DIR,
        "emulation_system/resources/vagrant/settings.json"
    )
    CREATE_COMMAND_NAME = "Create"
    SHELL_COMMAND_NAME = "Shell"
    REMOVE_COMMAND_NAME = "Remove"

    command: str
    mode: str
    dry_run: bool = False

    def __post_init__(self):
        self.command_mapping = {
            VirtualMachineSubCommands.CREATE.value: self.create,
            VirtualMachineSubCommands.SHELL.value: self.shell,
            VirtualMachineSubCommands.REMOVE.value: self.remove,
        }
        if self.command not in self.command_mapping.keys():
            command_string = ', '.join(self.VALID_COMMANDS)
            raise InvalidCommandError(
                f"\"command\" must be one of the following values: {command_string}"
            )

    @classmethod
    def from_cli_input(
            cls, args: argparse.Namespace, settings: ConfigurationSettings
    ) -> VirtualMachineCreator:
        cls._create_json_settings_file(settings)
        return cls(
            command=args.vm_command,
            mode=args.mode,
            dry_run=args.dry_run
        )

    @classmethod
    def _create_json_settings_file(cls, settings_object: ConfigurationSettings) -> None:
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
            NUM_SOCKET_CAN_NETWORKS=vm_settings.num_socket_can_networks
        ).json(indent=4)

        settings_file = open(cls.SETTINGS_FILE_LOCATION, 'w')
        settings_file.write(json_output)
        settings_file.close()

    def get_commands(self) -> CommandList:
        return CommandList(
            command_list=[self.command_mapping[self.command]()],
            dry_run=self.dry_run
        )

    def create(self) -> Command:
        return Command(
            command_name=self.CREATE_COMMAND_NAME,
            command=f"vagrant up {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION
        )

    def shell(self) -> Command:
        return Command(
            command_name=self.SHELL_COMMAND_NAME,
            command=f"vagrant ssh {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION
        )

    def remove(self) -> Command:
        return Command(
            command_name=self.REMOVE_COMMAND_NAME,
            command=f"vagrant destroy --force {self.mode}",
            cwd=self.VAGRANT_RESOURCES_LOCATION
        )

