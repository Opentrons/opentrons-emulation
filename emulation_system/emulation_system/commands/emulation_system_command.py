"""Command for accessing compose_file_creator."""

from __future__ import annotations

import argparse
import io
import os
from dataclasses import dataclass

import yaml

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)

STDIN_NAME = "<stdin>"
STDOUT_NAME = "<stdout>"


class InvalidFormatPassedToStdinException(Exception):
    """Exception raised when invalid format is passed."""

    ...


class InvalidFileExtensionException(Exception):
    """Exception raise when file passed does not have yaml or json extension."""


@dataclass
class EmulationSystemCommand:
    """Connection point between cli and compose_file_creator."""

    input_path: io.TextIOWrapper
    output_path: io.TextIOWrapper

    @classmethod
    def from_cli_input(
        cls, args: argparse.Namespace, settings: OpentronsEmulationConfiguration
    ) -> EmulationSystemCommand:
        """Construct EmulationSystemCommand from CLI input."""
        return cls(input_path=args.input_path, output_path=args.output_path)

    def execute(self) -> None:
        """Parse input file to compose file."""
        extension = os.path.splitext(self.input_path.name)[1]

        if self.input_path.name == STDIN_NAME or extension in [".yaml", ".json"]:
            stdin_content = self.input_path.read().strip()
            parsed_content = yaml.safe_load(stdin_content)
            if not isinstance(parsed_content, dict):
                raise InvalidFormatPassedToStdinException(
                    f'"{stdin_content}" is not valid yaml or JSON'
                )

            converted_object = convert_from_obj(parsed_content)
        else:
            raise InvalidFileExtensionException(
                "Passed file must either be a .json or" ".yaml extension."
            )

        self.output_path.write(converted_object.to_yaml())
