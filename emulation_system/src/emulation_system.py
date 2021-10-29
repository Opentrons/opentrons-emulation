import argparse
from textwrap import dedent
from script_creators.emulation_creator import EmulationOptions, EmulationCreator
from parser_utils import ParserWithError, get_formatter


class CLI:

    EMULATOR_COMMAND = "emulator"
    EMULATOR_ALIASES = ["em"]

    def __init__(self):
        self._parser = ParserWithError(description=self.DESCRIPTION)
        self._parser.add_argument()

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
        cls._vagrant(subparsers)
        cls._emulation(subparsers)
        cls._repo(subparsers)

        return parser

    @staticmethod
    def _emulation(parser: ParserWithError) -> None:
        emulation_parser = parser.add_parser(
            'emulator',
            aliases=['em'],
            help="Create emulated system",
            formatter_class=get_formatter(),

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
    def _vagrant(parser: ParserWithError) -> None:
        subparser = parser.add_parser(
            'virtual-machine',
            aliases=['vm'],
            formatter_class=get_formatter(),
            help="Create and manage virtual machines",
        )
        sub_subparser = subparser.add_subparsers(
            # help="Virtual Machine sub-commands",
            dest="vm_command",
            title="Virtual Machine Sub Commands",
            required=True
        )
        sub_subparser.metavar = ''

        sub_subparser.add_parser('create', help="Create virtual machine")
        sub_subparser.add_parser('start', help="Start virtual machine")
        sub_subparser.add_parser('stop', help="Stop virtual machine")
        sub_subparser.add_parser('shell', help="Open shell inside of virtual machine")
        sub_subparser.add_parser('remove', help="Remove virtual machine")

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
    if args.command is None:
        parser.print_help()

    valid_em_commands = [CLI.EMULATOR_COMMAND]
    valid_em_commands.extend(CLI.EMULATOR_ALIASES)

    if args.command in valid_em_commands:
        args.func(args)
