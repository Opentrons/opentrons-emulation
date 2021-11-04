import subprocess
from dataclasses import dataclass
from typing import List
from settings import ROOT_DIR


class CommandExecutionError(ValueError):
    """Thrown when there is an error executing a command"""
    pass


@dataclass
class Command:
    """Command to be run by subprocess"""
    command_name: str
    command: str
    cwd: str = ROOT_DIR

    def run_command(self):
        try:
            command_output = subprocess.run(
                self.command,
                check=True,
                shell=True,
                cwd=self.cwd,
            )
        except subprocess.CalledProcessError as err:
            raise CommandExecutionError(err.stderr)
        else:
            return CommandOutput(
                command_name=self.command_name,
                command=command_output.args
            )


@dataclass
class CommandOutput:
    """Output from command run by subprocess"""
    command_name: str
    command: str
    # output: str


@dataclass
class CommandList:
    """List of commands for subprocess to run"""
    command_list: List[Command]

    def add_command(self, command: Command):
        self.command_list.append(command)

    def run_commands(self):
        return [
            command.run_command()
            for command
            in self.command_list
        ]

