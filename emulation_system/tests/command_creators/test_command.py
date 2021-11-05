import pytest
from emulation_system.src.command_creators.command import (
    Command,
    CommandList,
    CommandExecutionError
)


@pytest.fixture
def hello_world():
    return "echo \"Hello Cruel World\""


@pytest.fixture
def goodbye_world():
    return "echo \"Goodbye Cruel World\""


@pytest.fixture
def bad_command():
    return "echo This will surely fail\""


def test_good_command(hello_world):
    command_name = "Good Command"
    output = Command(command_name=command_name, command=hello_world).run_command()
    assert output.command_name == command_name
    assert output.command == hello_world


def test_bad_command(bad_command):
    command_name = "Bad Command"
    with pytest.raises(CommandExecutionError):
        Command(command_name=command_name, command=bad_command).run_command()


def test_command_list(hello_world, goodbye_world):
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
