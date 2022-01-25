"""Parser for virtual-machine sub-command."""
import argparse
from emulation_system.parser_utils import get_formatter
from emulation_system.commands.virtual_machine_command import (
    VirtualMachineCommand,
    VirtualMachineSubCommandOptions,
    VirtualMachineSubCommands,
)
from emulation_system.parsers.abstract_parser import AbstractParser
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)


class VirtualMachineParser(AbstractParser):
    """Parser for virtual-machine sub-command."""

    @classmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: OpentronsEmulationConfiguration
    ) -> None:
        """Build parser for virtual-machine command."""
        subparser = parser.add_parser(  # type: ignore
            "virtual-machine",
            aliases=["vm"],
            formatter_class=get_formatter(),
            help="Create and manage virtual machines",
        )

        sub_subparser = subparser.add_subparsers(
            dest="vm_command", title="Virtual Machine Sub Commands", required=True
        )
        sub_subparser.metavar = ""

        common_parser = argparse.ArgumentParser()
        common_parser.set_defaults(func=VirtualMachineCommand.from_cli_input)
        common_parser.add_argument(
            VirtualMachineSubCommandOptions.MODE.value,
            action="store",
            help="Run as production or development system",
            choices=["prod", "dev"],
        )

        sub_subparser.add_parser(
            VirtualMachineSubCommands.CREATE.value,
            help="Create virtual machine",
            parents=[common_parser],
            conflict_handler="resolve",
        )

        sub_subparser.add_parser(
            VirtualMachineSubCommands.SHELL.value,
            help="Open shell inside of virtual machine",
            parents=[common_parser],
            conflict_handler="resolve",
        )

        sub_subparser.add_parser(
            VirtualMachineSubCommands.REMOVE.value,
            help="Remove virtual machine",
            parents=[common_parser],
            conflict_handler="resolve",
        )
