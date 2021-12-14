"""Abstract Class for all command creator classes to inherit from."""
from __future__ import annotations
import abc
import argparse

from emulation_system.commands.command import CommandList
from emulation_system.settings_models import ConfigurationSettings


class AbstractCommandCreator(abc.ABC):
    """Abstract Class for all command creator classes to inherit from."""

    @classmethod
    @abc.abstractmethod
    def from_cli_input(
        cls, args: argparse.Namespace, settings: ConfigurationSettings
    ) -> AbstractCommandCreator:
        """Parse cli input args into Command Creator class."""
        ...

    @abc.abstractmethod
    def get_commands(self) -> CommandList:
        """Get list of commands to be run."""
        ...
