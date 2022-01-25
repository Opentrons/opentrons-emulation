"""Top-level parser for emulation cli."""
import argparse
import sys
from emulation_system.executable import Executable
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from emulation_system.parser_utils import get_formatter
from emulation_system.parsers.emulation_parser import EmulationParser
from emulation_system.parsers.emulation_system_parser import EmulationSystemParser
from emulation_system.parsers.repo_parser import RepoParser
from emulation_system.parsers.virtual_machine_parser import VirtualMachineParser


class TopLevelParser:
    """Top-level parser for emulation cli.

    All commands should be a subcommand of this parser.
    """

    # Add subcommand parsers here
    # Parsers must inherit from emulation_system/src/parsers/abstract_parser.py
    SUBPARSERS = [
        EmulationParser,
        RepoParser,
        VirtualMachineParser,
        EmulationSystemParser,
    ]

    def __init__(self, settings: OpentronsEmulationConfiguration) -> None:
        """Construct TopLevelParser object.

        Pull settings from settings file
        Build parser
        """
        self._settings = settings
        self._parser = argparse.ArgumentParser(
            description="Utility for managing Opentrons Emulation systems",
            formatter_class=get_formatter(),
            prog="opentrons-emulation",
        )

        self._parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print out commands to be run by system",
        )

        subparsers = self._parser.add_subparsers(
            dest="command", title="subcommands", required=True
        )

        for subparser in self.SUBPARSERS:
            subparser.get_parser(subparsers, self._settings)  # type: ignore

    def parse(self, passed_args=[]) -> Executable:  # noqa: ANN001
        """Parse args into CommandCreator."""
        if len(passed_args) == 0:
            parsed_args = self._parser.parse_args(sys.argv[1:])
        else:
            parsed_args = self._parser.parse_args(passed_args)

        return parsed_args.func(parsed_args, self._settings)
