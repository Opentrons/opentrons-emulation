import argparse
from emulation_system.parser_utils import get_formatter
from emulation_system.parsers.abstract_parser import AbstractParser
from emulation_system.settings import LATEST_KEYWORD
from emulation_system.settings_models import ConfigurationSettings
from emulation_system.commands.emulation_command_creator import (
    CommonEmulationOptions,
    ProductionEmulationOptions,
    DevelopmentEmulationOptions,
    EmulationSubCommands,
    ProdEmulationCommandCreator,
    DevEmulationCommandCreator,
)
from emulation_system.os_state import OSState


class EmulationParser(AbstractParser):
    """Parser for emulation sub-command"""

    @classmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: ConfigurationSettings
    ) -> None:
        """Build parser for emulation command"""

        em_parser = parser.add_parser(  # type: ignore
            "emulator",
            aliases=["em"],
            help="Create emulated system",
            formatter_class=get_formatter(),
        )
        sub_subparser = em_parser.add_subparsers(
            dest="em_command", title="Emulation Sub Commands", required=True
        )

        common_parser = argparse.ArgumentParser()
        common_parser.add_argument(
            f"{CommonEmulationOptions.DETACHED.value}",
            action="store_true",
            help="Release stdout after emulation system creation",
        )

        prod_parser = sub_subparser.add_parser(
            EmulationSubCommands.PROD_MODE.value,
            help="Create production system",
            parents=[common_parser],
            conflict_handler="resolve",
            formatter_class=get_formatter(),
        )
        prod_parser.set_defaults(func=ProdEmulationCommandCreator.from_cli_input)
        prod_parser.add_argument(
            f"{ProductionEmulationOptions.OT3_FIRMWARE_SHA.value}",
            action="store",
            help="Commit ID to download from ot3-firmware repo",
            metavar="<commit-sha>",
            default=LATEST_KEYWORD,
        )
        prod_parser.add_argument(
            f"{ProductionEmulationOptions.MODULES_SHA.value}",
            action="store",
            help="Commit ID to download from opentrons-modules repo",
            metavar="<commit-sha>",
            default=LATEST_KEYWORD,
        )
        prod_parser.add_argument(
            f"{ProductionEmulationOptions.MONOREPO_SHA.value}",
            action="store",
            help="Commit ID to download from opentrons repo",
            metavar="<commit-sha>",
            default=LATEST_KEYWORD,
        )

        dev_parser = sub_subparser.add_parser(
            EmulationSubCommands.DEV_MODE.value,
            help="Create development system",
            parents=[common_parser],
            conflict_handler="resolve",
            formatter_class=get_formatter(),
        )
        dev_parser.set_defaults(func=DevEmulationCommandCreator.from_cli_input)
        dev_parser.add_argument(
            DevelopmentEmulationOptions.MODULES_PATH.value,
            help="Path to opentrons-modules repo source code",
            default=OSState().parse_path(settings.global_settings.default_folder_paths.modules),
            metavar="<absolute_path>",
        )
        dev_parser.add_argument(
            DevelopmentEmulationOptions.OT3_FIRMWARE_PATH.value,
            help="Path to ot3-firmware repo source code",
            default=OSState().parse_path(settings.global_settings.default_folder_paths.ot3_firmware),
            metavar="<absolute_path>",
        )
        dev_parser.add_argument(
            DevelopmentEmulationOptions.OPENTRONS_REPO.value,
            help="Path to opentrons repo source code",
            default=OSState().parse_path(settings.global_settings.default_folder_paths.opentrons),
            metavar="<absolute_path>",
        )
