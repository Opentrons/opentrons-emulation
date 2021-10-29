import argparse
from parser_utils import ParserWithError, get_formatter
from script_creators.emulation_creator import (
    EmulationOptions,
    EmulationSubCommands,
    ProdEmulationCreator,
    DevEmulationCreator
)


def emulation_parser(parser: ParserWithError) -> None:
    em_parser = parser.add_parser(
        'emulator',
        aliases=['em'],
        help="Create emulated system",
        formatter_class=get_formatter()
    )
    sub_subparser = em_parser.add_subparsers(
        dest="em_command",
        title="Emulation Sub Commands",
        required=True
    )

    common_parser = argparse.ArgumentParser()

    common_parser.add_argument(
        f"--{EmulationOptions.DETACHED.value}",
        action="store_true",
        help="Release stdout after emulation system creation"
    )

    prod_parser = sub_subparser.add_parser(
        EmulationSubCommands.PROD_MODE.value,
        help="Create production system",
        parents=[common_parser],
        conflict_handler='resolve'
    )
    prod_parser.set_defaults(func=ProdEmulationCreator.from_cli_input)
    prod_parser.add_argument(
        f"--{EmulationOptions.OT3_FIRMWARE_SHA.value}",
        action="store",
        help=(
            "Commit ID to download from ot3-firmware "
            "(Only for \"prod\" systems)"
        ),

    )
    prod_parser.add_argument(
        f'--{EmulationOptions.MODULES_SHA.value}',
        action="store",
        help=(
            "Commit ID to download from opentrons-modules "
            "(Only for \"prod\" systems)"
        )
    )

    dev_parser = sub_subparser.add_parser(
        EmulationSubCommands.DEV_MODE.value,
        help="Create development system",
        parents=[common_parser],
        conflict_handler='resolve'
    )
    dev_parser.set_defaults(func=DevEmulationCreator.from_cli_input)