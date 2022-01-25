from typing_extensions import Protocol


class Executable(Protocol):
    def execute(self) -> None:
        ...
