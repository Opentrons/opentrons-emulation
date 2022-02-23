"""Parser for virtual-machine sub-command."""
import argparse

from emulation_system.commands.emulation_system_command import EmulationSystemCommand
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from emulation_system.parser_utils import get_formatter
from emulation_system.parsers.abstract_parser import AbstractParser


class EmulationSystemParser(AbstractParser):
    """Parser for virtual-machine sub-command."""

    @classmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: OpentronsEmulationConfiguration
    ) -> None:
        """Build parser for "emulation-system" command."""
        subparser = parser.add_parser(  # type: ignore
            "emulation-system",
            aliases=["em-sys"],
            formatter_class=get_formatter(),
            help="Create docker-compose files",
        )

        subparser.set_defaults(func=EmulationSystemCommand.from_cli_input)

        subparser.add_argument(
            "input_path",
            action="store",
            metavar="<input_path>",
            type=argparse.FileType("r"),
            help='Input path to read file from. Specify "-" to read from stdin.',
        )

        subparser.add_argument(
            "output_path",
            action="store",
            metavar="<output_path>",
            type=argparse.FileType("w"),
            help='Output path write compose file to. Specify "-" to write to stdout.',
        )

        subparser.add_argument(
            "--remote-only", action="store_true", help="Allow only remote source-types"
        )
