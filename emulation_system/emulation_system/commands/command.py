"""All components necessary to run a single cli command."""

import os
import shlex
import subprocess
from dataclasses import dataclass, field
from typing import List, Dict
from emulation_system.consts import ROOT_DIR


class CommandExecutionError(ValueError):
    """Thrown when there is an error executing a command."""

    pass


@dataclass
class CommandOutput:
    """Dataclass for the output of a command run by subprocess."""

    command_name: str
    command: str
    command_output: str


@dataclass
class Command:
    """Command to be run by subprocess."""

    command_name: str
    command: str
    cwd: str = ROOT_DIR
    env: Dict = field(default_factory=dict)
    shell: bool = False

    @staticmethod
    def _capture_and_print_output(process: subprocess.Popen) -> str:
        """Capture command output in a list of strings and print it to stdout.

        Return single string containing all output at end.
        """
        stdout = []
        while True:
            output = process.stdout
            if output is None:
                continue
            line = output.readline().strip()
            stdout.append(line)
            print(line)
            if line == "" and process.poll() is not None:
                break
        return "".join(stdout)

    @staticmethod
    def _gen_env(var_dict: Dict[str, str]) -> Dict[str, str]:
        """Returns copy of current os env vars with this classes added to it."""
        env_copy = os.environ.copy()
        env_copy.update(var_dict)
        return env_copy

    def get_command_str(self) -> str:
        """Get command string that subshells to cwd and executes command."""
        env_string = ""
        if len(self.env) != 0:
            env_string = " ".join(f"{key}={value}" for key, value in self.env.items())

        return f"(cd {self.cwd} && {env_string} {self.command})"

    def _get_shell(self) -> None:
        """Opens shell to command that is run."""
        subprocess.Popen(
            shlex.split(self.command),
            text=True,
            cwd=self.cwd,
            env=self._gen_env(self.env),
        ).communicate()

    def _get_command(self):  # noqa: ANN202
        """Run command in subprocess and return output."""
        try:
            return subprocess.Popen(
                shlex.split(self.command),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.cwd,
                env=self._gen_env(self.env),
            )
        except subprocess.CalledProcessError as err:
            raise CommandExecutionError(err.stderr)

    def run_command(self) -> CommandOutput:
        """Execute shell command using subprocess. and return output."""
        if self.shell:
            self._get_shell()
            output = CommandOutput(
                command_name=self.command_name,
                command=self.command,
                command_output="Shell finished",
            )
        else:
            p = self._get_command()
            output = CommandOutput(
                command_name=self.command_name,
                command=self.command,
                command_output=self._capture_and_print_output(p),
            )

        return output


@dataclass
class CommandList:
    """List of commands for subprocess to run."""

    command_list: List[Command]
    dry_run: bool = False

    def add_command(self, command: Command) -> None:
        """Add command to list of commands to run."""
        self.command_list.append(command)

    def run_commands(self) -> List[CommandOutput]:
        """Run commands in shell. Prints output to stdout."""
        if self.dry_run:
            print("\n".join(command.get_command_str() for command in self.command_list))
            return []
        else:
            return [command.run_command() for command in self.command_list]
