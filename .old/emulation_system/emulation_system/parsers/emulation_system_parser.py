"""Parser for virtual-machine sub-command."""
import argparse

from emulation_system.commands import EmulationSystemCommand

from .abstract_parser import AbstractParser
from .parser_utils import get_formatter


class EmulationSystemParser(AbstractParser):
    """Parser for virtual-machine sub-command."""

    @classmethod
    def get_parser(cls, parser: argparse.ArgumentParser) -> None:
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

        subparser.add_argument(
            "--dev", action="store_true", help="Create dev compose file"
        )
