from __future__ import annotations
import abc
from command_creators.command import CommandList
from settings_models import ConfigurationSettings


class AbstractCommandCreator(abc.ABC):
    """Interface for AbstractCommandCreator classes"""
    @classmethod
    def from_cli_input(
            cls, args, settings: ConfigurationSettings
    ) -> AbstractCommandCreator:
        ...

    @abc.abstractmethod
    def get_commands(self) -> CommandList:
        ...