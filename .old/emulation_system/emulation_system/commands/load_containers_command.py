"""Command for loading containers from a configuration file."""

from __future__ import annotations

import argparse
import io
import os
from dataclasses import dataclass
from typing import cast

import yaml

from emulation_system.commands.emulation_system_command import (
    STDIN_NAME,
    InvalidFileExtensionException,
)

from ..compose_file_creator.conversion.conversion_functions import convert_from_obj


@dataclass
class LoadContainersCommand:
    """Connection point between cli and compose_file_creator."""

    input_path: io.TextIOWrapper
    filter: str
    local_only: bool

    @classmethod
    def from_cli_input(cls, args: argparse.Namespace) -> LoadContainersCommand:
        """Construct EmulationSystemCommand from CLI input."""
        return cls(
            input_path=args.input_path,
            filter=args.filter,
            local_only=args.local_only,
        )

    def execute(self) -> None:
        """Parse input file, apply filter, and print container names."""
        extension = os.path.splitext(self.input_path.name)[1]

        if self.input_path.name != STDIN_NAME and extension not in [".yaml", ".json"]:
            raise InvalidFileExtensionException(
                "Passed file must either be a .json or" ".yaml extension."
            )
        stdin_content = self.input_path.read().strip()
        parsed_content = yaml.safe_load(stdin_content)
        system = convert_from_obj(parsed_content, False)
        print(
            "\n".join(
                cast(str, container.container_name)
                for container in system.load_containers_by_filter(self.filter)
            )
        )
