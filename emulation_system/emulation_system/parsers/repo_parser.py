"""Parser for aws-ecr sub-command."""

import argparse

from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from emulation_system.parsers.abstract_parser import AbstractParser


class RepoParser(AbstractParser):
    """Parser for aws-ecr sub-command."""

    @classmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: OpentronsEmulationConfiguration
    ) -> None:
        """Build parser for aws-ecr command."""
        pass
