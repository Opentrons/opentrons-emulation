"""Abstract Base Class which all parsers should inherit from."""
import abc
import argparse
from emulation_system.opentrons_emulation_configuration import OpentronsEmulationConfiguration


class AbstractParser(abc.ABC):
    """Parser interface."""

    @classmethod
    @abc.abstractmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: OpentronsEmulationConfiguration
    ) -> None:
        """Method to return parser to add to argparse object."""
        ...
