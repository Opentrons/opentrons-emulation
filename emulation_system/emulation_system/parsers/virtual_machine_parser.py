"""Parser for virtual-machine sub-command."""
import argparse

from emulation_system.commands.virtual_machine_command import VirtualMachineCommand
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from emulation_system.parser_utils import get_formatter
from emulation_system.parsers.abstract_parser import AbstractParser


class VirtualMachineParser(AbstractParser):
    """Parser for virtual-machine sub-command."""

    @classmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: OpentronsEmulationConfiguration
    ) -> None:
        """Build parser for virtual-machine command."""
        subparser = parser.add_parser(  # type: ignore
            "virtual-machine",
            aliases=["vm"],
            formatter_class=get_formatter(),
            help="Create and manage virtual machines",
        )
        subparser.set_defaults(func=VirtualMachineCommand.from_cli_input)
