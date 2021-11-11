import argparse
from settings_models import ConfigurationSettings
from parsers.abstract_parser import AbstractParser


class RepoParser(AbstractParser):
    """Parser for aws-ecr sub-command"""

    @classmethod
    def get_parser(
            cls, parser: argparse.ArgumentParser, settings: ConfigurationSettings
    ) -> None:
        """Build parser for aws-ecr command"""
        parser.add_parser(
            'aws-ecr',
            help="Manage remote AWS ECR Docker image repo",
            aliases=['repo']
        )