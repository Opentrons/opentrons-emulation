"""Interface for executable things."""
from typing_extensions import Protocol


class Executable(Protocol):
    """Interface allowing things to be 'executed'."""

    def execute(self) -> None:
        """Execute something."""
        ...
