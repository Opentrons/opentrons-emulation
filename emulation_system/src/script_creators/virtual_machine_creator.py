from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class VirtualMachineSubCommands(str, Enum):
    CREATE = "create"
    START = "start"
    STOP = "stop"
    SHELL = "shell"
    REMOVE = "remove"


class VirtualMachineSubCommandOptions(str, Enum):
    MODE = "mode"


class InvalidCommandError(ValueError):
    pass


@dataclass
class VirtualMachineCreator:
    command: str
    mode: str


    @classmethod
    def from_cli_input(cls, args) -> None:
        return cls(
            command=args.vm_command,
            mode=args.mode
        ).run_command()

    def __post_init__(self):
        self.command_mapping = {
            VirtualMachineSubCommands.CREATE.value: self.create,
            VirtualMachineSubCommands.START.value: self.start,
            VirtualMachineSubCommands.STOP.value: self.stop,
            VirtualMachineSubCommands.SHELL.value: self.shell,
            VirtualMachineSubCommands.REMOVE.value: self.remove,
        }
        if self.command not in self.command_mapping.keys():
            command_string = ', '.join(self.VALID_COMMANDS)
            raise InvalidCommandError(
                f"\"command\" must be one of the following values: {command_string}"
            )

    def run_command(self):
        self.command_mapping[self.command]()

    def create(self):
        print(f"Creating {self.mode}")

    def start(self):
        print(f"Starting {self.mode}")

    def stop(self):
        print(f"Stopping {self.mode}")

    def shell(self):
        print(f"Shelling {self.mode}")

    def remove(self):
        print(f"Removing {self.mode}")
