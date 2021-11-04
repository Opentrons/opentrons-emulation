import argparse
import os
import sys

from command_creators.abstract_command_creator import AbstractCommandCreator
from parser_utils import get_formatter
from parsers.emulation_parser import EmulationParser
from parsers.repo_parser import RepoParser
from parsers.virtual_machine_parser import VirtualMachineParser
from settings import (
    CONFIGURATION_FILE_LOCATION_VAR_NAME,
    DEFAULT_CONFIGURATION_FILE_PATH
)
from settings_models import ConfigurationSettings


class TopLevelParser:
    """Top-level parser for emulation cli.
    All commands should be a subcommand of this parser"""

    # Add subcommand parsers here
    # Parsers must inherit from emulation_system/src/parsers/abstract_parser.py
    SUBPARSERS = [
        EmulationParser,
        RepoParser,
        VirtualMachineParser
    ]

    def __init__(self):
        self._settings = self._get_settings()
        self._parser = argparse.ArgumentParser(
            description="Utility for managing Opentrons Emulation systems",
            formatter_class=get_formatter(),
            prog="opentrons-emulation",
        )

        subparsers = self._parser.add_subparsers(
            dest="command", title="subcommands", required=True
        )

        for subparser in self.SUBPARSERS:
            subparser.get_parser(subparsers, self._settings)

    @staticmethod
    def _get_settings() -> ConfigurationSettings:
        if CONFIGURATION_FILE_LOCATION_VAR_NAME in os.environ:
            file_path = os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME]
        else:
            file_path = DEFAULT_CONFIGURATION_FILE_PATH

        return ConfigurationSettings.from_file_path(file_path)

    def parse(self, passed_args=[]) -> AbstractCommandCreator:
        if len(passed_args) == 0:
            parsed_args = self._parser.parse_args(sys.argv[1:])
        else:
            parsed_args = self._parser.parse_args(passed_args)

        return parsed_args.func(parsed_args, self._settings)
