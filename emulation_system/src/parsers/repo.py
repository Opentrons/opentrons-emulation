import argparse


def repo_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_parser(
        'aws-ecr',
        help="Manage remote AWS ECR Docker image repo",
        aliases=['repo']
    )