import pytest
from typing import List
from emulation_system.command_creators.virtual_machine_creator import (
    VirtualMachineCreator
)
from emulation_system.command_creators.command import CommandList, Command
from emulation_system.parsers.top_level_parser import TopLevelParser

EXPECTED_DEV_CREATE = CommandList(
    [
        Command(
            command_name=VirtualMachineCreator.CREATE_COMMAND_NAME,
            command="vagrant up dev",
            cwd=VirtualMachineCreator.VAGRANT_RESOURCES_LOCATION
        )
    ]
)
EXPECTED_DEV_REMOVE = CommandList(
    [
        Command(
            command_name=VirtualMachineCreator.REMOVE_COMMAND_NAME,
            command="vagrant destroy --force dev",
            cwd=VirtualMachineCreator.VAGRANT_RESOURCES_LOCATION
        )
    ]
)
EXPECTED_DEV_SHELL = CommandList(
    [
        Command(
            command_name=VirtualMachineCreator.SHELL_COMMAND_NAME,
            command="vagrant ssh dev",
            cwd=VirtualMachineCreator.VAGRANT_RESOURCES_LOCATION
        )
    ]
)
EXPECTED_PROD_CREATE = CommandList(
    [
        Command(
            command_name=VirtualMachineCreator.CREATE_COMMAND_NAME,
            command="vagrant up prod",
            cwd=VirtualMachineCreator.VAGRANT_RESOURCES_LOCATION
        )
    ]
)
EXPECTED_PROD_REMOVE = CommandList(
    [
        Command(
            command_name=VirtualMachineCreator.REMOVE_COMMAND_NAME,
            command="vagrant destroy --force prod",
            cwd=VirtualMachineCreator.VAGRANT_RESOURCES_LOCATION
        )
    ]
)
EXPECTED_PROD_SHELL = CommandList(
    [
        Command(
            command_name=VirtualMachineCreator.SHELL_COMMAND_NAME,
            command="vagrant ssh prod",
            cwd=VirtualMachineCreator.VAGRANT_RESOURCES_LOCATION
        )
    ]
)


@pytest.fixture
def dev_create_virtual_machine_cmd() -> List[str]:
    return "vm create dev".split(" ")


@pytest.fixture
def dev_remove_virtual_machine_cmd() -> List[str]:
    return "vm remove dev".split(" ")


@pytest.fixture
def dev_shell_virtual_machine_cmd() -> List[str]:
    return "vm shell dev".split(" ")


@pytest.fixture
def prod_create_virtual_machine_cmd() -> List[str]:
    return "vm create prod".split(" ")


@pytest.fixture
def prod_remove_virtual_machine_cmd() -> List[str]:
    return "vm remove prod".split(" ")


@pytest.fixture
def prod_shell_virtual_machine_cmd() -> List[str]:
    return "vm shell prod".split(" ")


def test_dev_create(dev_create_virtual_machine_cmd):
    cmds = TopLevelParser().parse(dev_create_virtual_machine_cmd).get_commands()
    assert cmds == EXPECTED_DEV_CREATE


def test_dev_shell(dev_shell_virtual_machine_cmd):
    cmds = TopLevelParser().parse(dev_shell_virtual_machine_cmd).get_commands()
    assert cmds == EXPECTED_DEV_SHELL


def test_dev_remove(dev_remove_virtual_machine_cmd):
    cmds = TopLevelParser().parse(dev_remove_virtual_machine_cmd).get_commands()
    assert cmds == EXPECTED_DEV_REMOVE


def test_prod_create(prod_create_virtual_machine_cmd):
    cmds = TopLevelParser().parse(prod_create_virtual_machine_cmd).get_commands()
    assert cmds == EXPECTED_PROD_CREATE


def test_prod_shell(prod_shell_virtual_machine_cmd):
    cmds = TopLevelParser().parse(prod_shell_virtual_machine_cmd).get_commands()
    assert cmds == EXPECTED_PROD_SHELL


def test_prod_remove(prod_remove_virtual_machine_cmd):
    cmds = TopLevelParser().parse(prod_remove_virtual_machine_cmd).get_commands()
    assert cmds == EXPECTED_PROD_REMOVE
