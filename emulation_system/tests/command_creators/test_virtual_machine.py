"""Tests for virtual-machine sub-command."""
import pytest
from typing import List
from emulation_system.commands.virtual_machine_command import (
    VirtualMachineCommand,
)
from emulation_system.commands.sub_process_command import (
    SubProcessCommandList,
    SubProcessCommand,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from emulation_system.parsers.top_level_parser import TopLevelParser

EXPECTED_DEV_CREATE = SubProcessCommandList(
    [
        SubProcessCommand(
            command_name=VirtualMachineCommand.CREATE_COMMAND_NAME,
            command="vagrant up dev",
            cwd=VirtualMachineCommand.VAGRANT_RESOURCES_LOCATION,
        )
    ]
)
EXPECTED_DEV_REMOVE = SubProcessCommandList(
    [
        SubProcessCommand(
            command_name=VirtualMachineCommand.REMOVE_COMMAND_NAME,
            command="vagrant destroy --force dev",
            cwd=VirtualMachineCommand.VAGRANT_RESOURCES_LOCATION,
        )
    ]
)
EXPECTED_DEV_SHELL = SubProcessCommandList(
    [
        SubProcessCommand(
            command_name=VirtualMachineCommand.SHELL_COMMAND_NAME,
            command="vagrant ssh dev",
            cwd=VirtualMachineCommand.VAGRANT_RESOURCES_LOCATION,
            shell=True,
        )
    ]
)
EXPECTED_PROD_CREATE = SubProcessCommandList(
    [
        SubProcessCommand(
            command_name=VirtualMachineCommand.CREATE_COMMAND_NAME,
            command="vagrant up prod",
            cwd=VirtualMachineCommand.VAGRANT_RESOURCES_LOCATION,
        )
    ]
)
EXPECTED_PROD_REMOVE = SubProcessCommandList(
    [
        SubProcessCommand(
            command_name=VirtualMachineCommand.REMOVE_COMMAND_NAME,
            command="vagrant destroy --force prod",
            cwd=VirtualMachineCommand.VAGRANT_RESOURCES_LOCATION,
        )
    ]
)
EXPECTED_PROD_SHELL = SubProcessCommandList(
    [
        SubProcessCommand(
            command_name=VirtualMachineCommand.SHELL_COMMAND_NAME,
            command="vagrant ssh prod",
            cwd=VirtualMachineCommand.VAGRANT_RESOURCES_LOCATION,
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
    testing_global_em_config: OpentronsEmulationConfiguration,
    dev_create_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that dev virtual-machine is created correctly."""
    cmds = TopLevelParser(testing_global_em_config).parse(
        dev_create_virtual_machine_cmd
    )
    assert cmds == EXPECTED_DEV_CREATE


def test_dev_shell(
    testing_global_em_config: OpentronsEmulationConfiguration,
    dev_shell_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that shell to dev virtual-machine is opened correctly."""
    cmds = TopLevelParser(testing_global_em_config).parse(dev_shell_virtual_machine_cmd)
    assert cmds == EXPECTED_DEV_SHELL


def test_dev_remove(
    testing_global_em_config: OpentronsEmulationConfiguration,
    dev_remove_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that dev virtual-machine is removed correctly."""
    cmds = TopLevelParser(testing_global_em_config).parse(
        dev_remove_virtual_machine_cmd
    )
    assert cmds == EXPECTED_DEV_REMOVE


def test_prod_create(
    testing_global_em_config: OpentronsEmulationConfiguration,
    prod_create_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that prod virtual-machine is created correctly."""
    cmds = TopLevelParser(testing_global_em_config).parse(
        prod_create_virtual_machine_cmd
    )
    assert cmds == EXPECTED_PROD_CREATE


def test_prod_shell(
    testing_global_em_config: OpentronsEmulationConfiguration,
    prod_shell_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that shell to prod virtual-machine is opened correctly."""
    cmds = TopLevelParser(testing_global_em_config).parse(
        prod_shell_virtual_machine_cmd
    )
    assert cmds == EXPECTED_PROD_SHELL


def test_prod_remove(
    testing_global_em_config: OpentronsEmulationConfiguration,
    prod_remove_virtual_machine_cmd: List[str],
) -> None:
    """Confirm that prod virtual-machine is removed correctly."""
    cmds = TopLevelParser(testing_global_em_config).parse(
        prod_remove_virtual_machine_cmd
    )
    assert cmds == EXPECTED_PROD_REMOVE
