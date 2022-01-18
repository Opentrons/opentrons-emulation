"""Tests for virtual-machine sub-command."""
import pytest
from typing import List
from emulation_system.commands.virtual_machine_command_creator import (
    VirtualMachineCommandCreator,
)
from emulation_system.commands.command import CommandList, Command
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from emulation_system.parsers.top_level_parser import TopLevelParser

EXPECTED_DEV_CREATE = CommandList(
    [
        Command(
            command_name=VirtualMachineCommandCreator.CREATE_COMMAND_NAME,
            command="vagrant up dev",
            cwd=VirtualMachineCommandCreator.VAGRANT_RESOURCES_LOCATION,
        )
    ]
)
EXPECTED_DEV_REMOVE = CommandList(
    [
        Command(
            command_name=VirtualMachineCommandCreator.REMOVE_COMMAND_NAME,
            command="vagrant destroy --force dev",
            cwd=VirtualMachineCommandCreator.VAGRANT_RESOURCES_LOCATION,
        )
    ]
)
EXPECTED_DEV_SHELL = CommandList(
    [
        Command(
            command_name=VirtualMachineCommandCreator.SHELL_COMMAND_NAME,
            command="vagrant ssh dev",
            cwd=VirtualMachineCommandCreator.VAGRANT_RESOURCES_LOCATION,
            shell=True,
        )
    ]
)
EXPECTED_PROD_CREATE = CommandList(
    [
        Command(
            command_name=VirtualMachineCommandCreator.CREATE_COMMAND_NAME,
            command="vagrant up prod",
            cwd=VirtualMachineCommandCreator.VAGRANT_RESOURCES_LOCATION,
        )
    ]
)
EXPECTED_PROD_REMOVE = CommandList(
    [
        Command(
            command_name=VirtualMachineCommandCreator.REMOVE_COMMAND_NAME,
            command="vagrant destroy --force prod",
            cwd=VirtualMachineCommandCreator.VAGRANT_RESOURCES_LOCATION,
        )
    ]
)
EXPECTED_PROD_SHELL = CommandList(
    [
        Command(
            command_name=VirtualMachineCommandCreator.SHELL_COMMAND_NAME,
            command="vagrant ssh prod",
            cwd=VirtualMachineCommandCreator.VAGRANT_RESOURCES_LOCATION,
            shell=True,
        )
    ]
)


@pytest.fixture
def dev_create_virtual_machine_cmd() -> List[str]:
    """Returns command to create dev vm."""
    return "vm create dev".split(" ")


@pytest.fixture
def dev_remove_virtual_machine_cmd() -> List[str]:
    """Returns command to remove dev vm."""
    return "vm remove dev".split(" ")


@pytest.fixture
def dev_shell_virtual_machine_cmd() -> List[str]:
    """Returns command to open shell to dev vm."""
    return "vm shell dev".split(" ")


@pytest.fixture
def prod_create_virtual_machine_cmd() -> List[str]:
    """Returns command to create prod vm."""
    return "vm create prod".split(" ")


@pytest.fixture
def prod_remove_virtual_machine_cmd() -> List[str]:
    """Returns command to remove prod vm."""
    return "vm remove prod".split(" ")


@pytest.fixture
def prod_shell_virtual_machine_cmd() -> List[str]:
    """Returns command to open shell prod vm."""
    return "vm shell prod".split(" ")


def test_dev_create(
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
    dev_create_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that dev virtual-machine is created correctly."""
    cmds = (
        TopLevelParser(testing_opentrons_emulation_configuration)
        .parse(dev_create_virtual_machine_cmd)
        .get_commands()
    )
    assert cmds == EXPECTED_DEV_CREATE


def test_dev_shell(
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
    dev_shell_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that shell to dev virtual-machine is opened correctly."""
    cmds = (
        TopLevelParser(testing_opentrons_emulation_configuration)
        .parse(dev_shell_virtual_machine_cmd)
        .get_commands()
    )
    assert cmds == EXPECTED_DEV_SHELL


def test_dev_remove(
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
    dev_remove_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that dev virtual-machine is removed correctly."""
    cmds = (
        TopLevelParser(testing_opentrons_emulation_configuration)
        .parse(dev_remove_virtual_machine_cmd)
        .get_commands()
    )
    assert cmds == EXPECTED_DEV_REMOVE


def test_prod_create(
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
    prod_create_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that prod virtual-machine is created correctly."""
    cmds = (
        TopLevelParser(testing_opentrons_emulation_configuration)
        .parse(prod_create_virtual_machine_cmd)
        .get_commands()
    )
    assert cmds == EXPECTED_PROD_CREATE


def test_prod_shell(
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
    prod_shell_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that shell to prod virtual-machine is opened correctly."""
    cmds = (
        TopLevelParser(testing_opentrons_emulation_configuration)
        .parse(prod_shell_virtual_machine_cmd)
        .get_commands()
    )
    assert cmds == EXPECTED_PROD_SHELL


def test_prod_remove(
    testing_opentrons_emulation_configuration: OpentronsEmulationConfiguration,
    prod_remove_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that prod virtual-machine is removed correctly."""
    cmds = (
        TopLevelParser(testing_opentrons_emulation_configuration)
        .parse(prod_remove_virtual_machine_cmd)
        .get_commands()
    )
    assert cmds == EXPECTED_PROD_REMOVE
