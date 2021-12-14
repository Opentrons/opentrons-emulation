"""Tests for Command class."""
import pytest
from emulation_system.commands.command import (
    Command,
    CommandList,
)


@pytest.fixture
def hello_world() -> str:
    """Creates a command to print "Hello World"."""
    return 'echo "Hello Cruel World"'


@pytest.fixture
def goodbye_world() -> str:
    """Creates a command to print "Goodbye World"."""
    return 'echo "Goodbye Cruel World"'


def test_good_command(hello_world: str) -> None:
    """Confirm valid Command works."""
    command_name = "Good Command"
    output = Command(command_name=command_name, command=hello_world).run_command()
    assert output.command_name == command_name
    assert output.command == hello_world


def test_comp() -> None:
    """Confirm comparing 2 commands for equality works."""
    name = "My Name"
    cmd = 'echo "Hello World"'
    assert Command(command_name=name, command=cmd) == Command(
        command_name=name, command=cmd
    )


def test_command_list(hello_world: str, goodbye_world: str) -> None:
    """Confirm valid CommandList works."""
    hello_world_command_name = "Hello World"
    hello_world_cmd = Command(
        command_name=hello_world_command_name, command=hello_world
    )
    goodbye_world_command_name = "Goodbye World"
    goodbye_world_cmd = Command(
        command_name=goodbye_world_command_name, command=goodbye_world
    )

    outputs = CommandList([hello_world_cmd, goodbye_world_cmd]).run_commands()

    assert outputs[0].command_name == hello_world_command_name
    assert outputs[0].command == hello_world

    assert outputs[1].command_name == goodbye_world_command_name
    assert outputs[1].command == goodbye_world
