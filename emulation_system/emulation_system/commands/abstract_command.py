"""Abstract Class for all command creator classes to inherit from."""
from __future__ import annotations

import abc
import argparse

from emulation_system.executable import Executable
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)


class AbstractCommand(abc.ABC):
    """Abstract Class for all command classes to inherit from."""

    @classmethod
    @abc.abstractmethod
    def from_cli_input(
        cls, args: argparse.Namespace, settings: OpentronsEmulationConfiguration
    ) -> Executable:
        """Parse cli input args into SubProcessCommand Creator class."""
        ...
