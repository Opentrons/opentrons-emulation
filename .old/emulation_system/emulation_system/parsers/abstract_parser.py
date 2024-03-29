"""Abstract Base Class which all parsers should inherit from."""
import abc
import argparse


class AbstractParser(abc.ABC):
    """Parser interface."""

    @classmethod
    @abc.abstractmethod
    def get_parser(cls, parser: argparse.ArgumentParser) -> None:
        """Method to return parser to add to argparse object."""
        ...
