import argparse
from textwrap import dedent
from script_creators.emulation_creator import EmulationOptions, EmulationCreator
from script_creators.virtual_machine_creator import (
    VirtualMachineSubCommands, VirtualMachineCreator, VirtualMachineSubCommandOptions
)
from parser_utils import ParserWithError, get_formatter


class CLI:

    EMULATOR_COMMAND = "emulator"
    EMULATOR_ALIASES = ["em"]

    VIRTUAL_MACHINE_COMMAND = 'virtual-machine'
    VIRTUAL_MACHINE_ALIASES = ['vm']

    @classmethod
    def parser(cls) -> ParserWithError:
        parser = ParserWithError(
            description="Utility for managing Opentrons Emulation system",
            formatter_class=get_formatter()
        )

        subparsers = parser.add_subparsers(
            dest="command", title="subcommands", required=True
        )
        subparsers.metavar = ''
        cls._vm(subparsers)
        cls._emulation(subparsers)
        cls._repo(subparsers)

        return parser

    @staticmethod
    def _emulation(parser: ParserWithError) -> None:
        emulation_parser = parser.add_parser(
            'emulator',
            aliases=['em'],
            help="Create emulated system",
            formatter_class=get_formatter()


        )
        emulation_parser.set_defaults(func=EmulationCreator.from_cli_input)
        emulation_parser.add_argument(
            EmulationOptions.MODE.value,
            action="store",
            help="Run as production or development system",
            choices=["prod", "dev"]
        )
        emulation_parser.add_argument(
            f"--{EmulationOptions.DETACHED.value}",
            action="store_true",
            help="Release stdout after emulation system creation"
        )
        emulation_parser.add_argument(
            f"--{EmulationOptions.OT3_FIRMWARE_SHA.value}",
            action="store",
            help=(
                "Commit ID to download from ot3-firmware "
                "(Only for \"prod\" systems)"
            ),

        )
        emulation_parser.add_argument(
            f'--{EmulationOptions.MODULES_SHA.value}',
            action="store",
            help=(
                "Commit ID to download from opentrons-modules "
                "(Only for \"prod\" systems)"
            )
        )

    @staticmethod
    def _vm(parser: ParserWithError) -> None:
        subparser = parser.add_parser(
            'virtual-machine',
            aliases=['vm'],
            formatter_class=get_formatter(),
            help="Create and manage virtual machines",
        )

        sub_subparser = subparser.add_subparsers(
            dest="vm_command",
            title="Virtual Machine Sub Commands",
            required=True
        )
        sub_subparser.metavar = ''

        common_parser = argparse.ArgumentParser()
        common_parser.add_argument(
            VirtualMachineSubCommandOptions.MODE.value,
            action="store",
            help="Run as production or development system",
            choices=["prod", "dev"]
        )
        common_parser.set_defaults(func=VirtualMachineCreator.from_cli_input)

        sub_subparser.add_parser(
            VirtualMachineSubCommands.CREATE.value,
            help="Create virtual machine",
            parents=[common_parser],
            conflict_handler='resolve'
        )
        sub_subparser.add_parser(
            VirtualMachineSubCommands.START.value,
            help="Start virtual machine",
            parents=[common_parser],
            conflict_handler='resolve'
        )
        sub_subparser.add_parser(
            VirtualMachineSubCommands.STOP.value,
            help="Stop virtual machine",
            parents=[common_parser],
            conflict_handler='resolve'
        )
        sub_subparser.add_parser(
            VirtualMachineSubCommands.SHELL.value,
            help="Open shell inside of virtual machine",
            parents=[common_parser],
            conflict_handler='resolve'

        )
        sub_subparser.add_parser(
            VirtualMachineSubCommands.REMOVE.value,
            help="Remove virtual machine",
            parents=[common_parser],
            conflict_handler='resolve'
        )

    @staticmethod
    def _repo(parser: ParserWithError) -> None:
        parser.add_parser(
            'aws-ecr',
            help="Manage remote AWS ECR Docker image repo",
            aliases=['repo']
        )

    def run(self):
        self._parser.parse_args()

if __name__ == "__main__":
    parser = CLI.parser()
    args = parser.parse_args()

    valid_em_commands = [CLI.EMULATOR_COMMAND]
    valid_em_commands.extend(CLI.EMULATOR_ALIASES)

    valid_vm_commands = [CLI.VIRTUAL_MACHINE_COMMAND]
    valid_vm_commands.extend(CLI.VIRTUAL_MACHINE_ALIASES)

    if args.command in valid_em_commands:
        print(args.func(args))
    elif args.command in valid_vm_commands:
        print(args.func(args))