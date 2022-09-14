"""Parser for virtual-machine sub-command."""
import argparse

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.commands import LoadContainersCommand

from .abstract_parser import AbstractParser
from .parser_utils import get_formatter


class LoadContainersParser(AbstractParser):
    """Parser for load-containers sub-command."""

    @classmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: OpentronsEmulationConfiguration
    ) -> None:
        """Build parser for "load-containers" command."""
        subparser = parser.add_parser(  # type: ignore
            "load-containers",
            aliases=["lc"],
            formatter_class=get_formatter(),
            help="Load Containers",
        )

        subparser.set_defaults(func=LoadContainersCommand.from_cli_input)

        subparser.add_argument(
            "--local-only",
            action="store_true",
            help="Filter to apply.",
        )

        subparser.add_argument(
            "input_path",
            action="store",
            metavar="<input_path>",
            type=argparse.FileType("r"),
            help='Input path to read file from. Specify "-" to read from stdin.',
        )

        subparser.add_argument(
            "filter",
            action="store",
            metavar="<filter>",
            help="Filter to apply.",
        )
