"""Tests for virtual-machine sub-command."""
import argparse
from unittest.mock import MagicMock
from pydantic import parse_obj_as
import pytest

from emulation_system.commands.virtual_machine_command import VirtualMachineCommand
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
    SharedFolder,
)


@pytest.fixture
def test_vm_command(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> VirtualMachineCommand:
    """Build testing version of VirtualMachineCommand."""
    mock = MagicMock(spec=argparse.Namespace)
    return VirtualMachineCommand.from_cli_input(mock, testing_global_em_config)


def test_get_virtual_machine_config(test_vm_command: VirtualMachineCommand) -> None:
    """Test that generating settings file works."""
    settings = test_vm_command.get_settings_obj()
    assert settings.VM_MEMORY == 4096
    assert settings.VM_CPUS == 2
    assert settings.NUM_SOCKET_CAN_NETWORKS == "2"
    assert settings.SHARED_FOLDERS == [
        parse_obj_as(
            SharedFolder,
            {
                "host-path": "/home/Documents/repos/opentrons",
                "vm-path": "/home/vagrant/opentrons",
            },
        ),
        parse_obj_as(
            SharedFolder,
            {
                "host-path": "/home/Documents/repos/ot3-firmware",
                "vm-path": "/home/vagrant/ot3-firmware",
            },
        ),
        parse_obj_as(
            SharedFolder,
            {
                "host-path": "/home/Documents/repos/opentrons-modules",
                "vm-path": "/home/vagrant/opentrons-modules",
            },
        ),
        parse_obj_as(
            SharedFolder,
            {
                "host-path": "/home/derek-maggio/Documents/repos/opentrons-emulation",
                "vm-path": "/home/vagrant/opentrons-emulation",
            },
        ),
    ]
