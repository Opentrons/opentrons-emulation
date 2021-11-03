import argparse
from parsers.abstract_parser import AbstractParser
from settings_models import ConfigurationSettings


class RepoParser(AbstractParser):

    @classmethod
    def get_parser(
            cls, parser: argparse.ArgumentParser, settings: ConfigurationSettings
    ) -> None:
        parser.add_parser(
            'aws-ecr',
            help="Manage remote AWS ECR Docker image repo",
            aliases=['repo']
        )