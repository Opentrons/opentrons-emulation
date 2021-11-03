from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from settings import DEFAULT_CONFIGURATION_FILE_PATH
from settings_models import ConfigurationSettings


class VirtualMachineSubCommands(str, Enum):
    CREATE = "create"
    SHELL = "shell"
    REMOVE = "remove"


class VirtualMachineSubCommandOptions(str, Enum):
    MODE = "mode"


class InvalidCommandError(ValueError):
    pass


@dataclass
class VirtualMachineCreator:

    VAGRANTFILE_LOCATION = "resources/vagrant/Vagrantfile"
    SETTINGS_FILE_LOCATION = "resources/vagrant/settings.json"

    command: str
    mode: str

    @classmethod
    def from_cli_input(cls, args) -> VirtualMachineCreator:
        return cls(
            command=args.vm_command,
            mode=args.mode
        )

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

    def run_command(self) -> str:
        return self.command_mapping[self.command]()

    def create(self) -> str:
        return f"vagrant up {self.mode}"

    def shell(self) -> str:
        return f"vagrant ssh {self.mode}"

    def remove(self) -> str:
        return f"vagrant destroy {self.mode}"

