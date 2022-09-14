"""Command for accessing compose_file_creator."""

from __future__ import annotations

import argparse
import io
import os
from dataclasses import dataclass

import yaml

from emulation_system import OpentronsEmulationConfiguration

from ..compose_file_creator.conversion.conversion_functions import convert_from_obj
from ..compose_file_creator.errors import NotRemoteOnlyError
from ..compose_file_creator.logging.console import logging_console

STDIN_NAME = "<stdin>"
STDOUT_NAME = "<stdout>"


class InvalidFileExtensionException(Exception):
    """Exception raise when file passed does not have yaml or json extension."""


@dataclass
class EmulationSystemCommand:
    """Connection point between cli and compose_file_creator."""

    input_path: io.TextIOWrapper
    output_path: io.TextIOWrapper
    remote_only: bool
    dev: bool
    settings: OpentronsEmulationConfiguration

    @classmethod
    def from_cli_input(
        cls, args: argparse.Namespace, settings: OpentronsEmulationConfiguration
    ) -> EmulationSystemCommand:
        """Construct EmulationSystemCommand from CLI input."""
        return cls(
            input_path=args.input_path,
            output_path=args.output_path,
            remote_only=args.remote_only,
            dev=args.dev,
            settings=settings,
        )

    def execute(self) -> None:
        """Parse input file to compose file."""
        extension = os.path.splitext(self.input_path.name)[1]

        if self.input_path.name != STDIN_NAME and extension not in [".yaml", ".json"]:
            raise InvalidFileExtensionException(
                "Passed file must either be a .json or" ".yaml extension."
            )
        stdin_content = self.input_path.read().strip()
        parsed_content = yaml.safe_load(stdin_content)
        converted_object = convert_from_obj(parsed_content, self.settings, self.dev)

        if self.remote_only and not converted_object.is_remote:
            raise NotRemoteOnlyError

        self.output_path.write(converted_object.to_yaml())
        logging_console.save_log()
