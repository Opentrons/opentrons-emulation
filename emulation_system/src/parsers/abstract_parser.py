import abc
import argparse
from settings_models import ConfigurationSettings

class AbstractParser(abc.ABC):

    @abc.abstractmethod
    def get_parser(
            cls, parser: argparse.ArgumentParser, settings: ConfigurationSettings
    ) -> None:
        ...
