from parser_utils import ParserWithError


def repo_parser(parser: ParserWithError) -> None:
    parser.add_parser(
        'aws-ecr',
        help="Manage remote AWS ECR Docker image repo",
        aliases=['repo']
    )