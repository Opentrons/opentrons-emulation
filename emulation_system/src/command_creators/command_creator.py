from __future__ import annotations
import abc
from command_creators.command import CommandList


class CommandCreator(abc.ABC):
    """Interface for CommandCreator classes"""
    @classmethod
    def from_cli_input(cls, args) -> CommandCreator:
        ...

    @abc.abstractmethod
    def get_commands(self) -> CommandList:
        ...