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

    def run_command(self) -> None:
        """Execute shell command using subprocess"""
        try:
            subprocess.run(
                self.command,
                check=True,
                shell=True,
                cwd=self.cwd,
            )
        except subprocess.CalledProcessError as err:
            raise CommandExecutionError(err.stderr)


@dataclass
class CommandList:
    """List of commands for subprocess to run"""
    command_list: List[Command]
    dry_run: bool = False

    def add_command(self, command: Command) -> None:
        """Add command to list of commands to run"""
        self.command_list.append(command)

    def _generate_dry_run(self) -> str:
        """Return runnable list of cli commands"""
        command_str_list = [
            f"(cd {command.cwd} && {command.command})"
            for command
            in self.command_list
        ]
        return '\n'.join(command_str_list)

    def run_commands(self) -> None:
        """Run commands in shell. Prints output to stdout"""
        if self.dry_run:
            print(self._generate_dry_run())
        else:
            for command in self.command_list:
                command.run_command()

