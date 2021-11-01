import argparse
from parser_utils import ParserWithError, get_formatter
from command_creators.emulation_creator import (
    CommonEmulationOptions,
    ProductionEmulationOptions,
    DevelopmentEmulationOptions,
    EmulationSubCommands,
    ProdEmulationCreator,
    DevEmulationCreator
)
from consts import (
    OPENTRONS_MODULES_REPO_DEFAULT_PATH,
    OT3_FIRMWARE_REPO_DEFAULT_PATH,
    OPENTRONS_REPO_DEFAULT_PATH
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
        f"--{CommonEmulationOptions.DETACHED.value}",
        action="store_true",
        help="Release stdout after emulation system creation"
    )

    prod_parser = sub_subparser.add_parser(
        EmulationSubCommands.PROD_MODE.value,
        help="Create production system",
        parents=[common_parser],
        conflict_handler='resolve',
        formatter_class=get_formatter()
    )
    prod_parser.set_defaults(func=ProdEmulationCreator.from_cli_input)
    prod_parser.add_argument(
        f"--{ProductionEmulationOptions.OT3_FIRMWARE_SHA.value}",
        action="store",
        help="Commit ID to download from ot3-firmware repo",
        metavar="<commit-sha>"
    )
    prod_parser.add_argument(
        f'--{ProductionEmulationOptions.MODULES_SHA.value}',
        action="store",
        help="Commit ID to download from opentrons-modules repo",
        metavar="<commit-sha>"
    )
    prod_parser.add_argument(
        f'--{ProductionEmulationOptions.MONOREPO_SHA.value}',
        action="store",
        help="Commit ID to download from opentrons repo",
        metavar="<commit-sha>"
    )

    dev_parser = sub_subparser.add_parser(
        EmulationSubCommands.DEV_MODE.value,
        help="Create development system",
        parents=[common_parser],
        conflict_handler='resolve',
        formatter_class=get_formatter()
    )
    dev_parser.set_defaults(func=DevEmulationCreator.from_cli_input)
    dev_parser.add_argument(
        DevelopmentEmulationOptions.MODULES_PATH.value,
        help="Path to opentrons-modules repo source code",
        default=OPENTRONS_MODULES_REPO_DEFAULT_PATH,
        metavar="<absolute_path>"
    )
    dev_parser.add_argument(
        DevelopmentEmulationOptions.OT3_FIRMWARE_PATH.value,
        help="Path to ot3-firmware repo source code",
        default=OT3_FIRMWARE_REPO_DEFAULT_PATH,
        metavar="<absolute_path>"
    )
    dev_parser.add_argument(
        DevelopmentEmulationOptions.OPENTRONS_REPO.value,
        help="Path to opentrons repo source code",
        default=OPENTRONS_REPO_DEFAULT_PATH,
        metavar="<absolute_path>"
    )