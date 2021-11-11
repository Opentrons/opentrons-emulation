import abc
import argparse
from emulation_system.settings_models import ConfigurationSettings


class AbstractParser(abc.ABC):
    """Parser interface"""

    @classmethod
    @abc.abstractmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: ConfigurationSettings
    ) -> None:
        ...
