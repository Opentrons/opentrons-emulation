"""Scripts for getting information about e2e tests."""

import argparse

from tests.e2e.system_mappings import get_test_ids, get_test_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interaction layer for opentrons-emulation e2e test mappings."
    )
    subparsers = parser.add_subparsers(dest="command")

    test_ids = subparsers.add_parser(
        "get-test-ids", help="Get list of available test IDs"
    )

    test_path = subparsers.add_parser(
        "get-test-path", help="Get path for test based on test ID"
    )
    test_path.add_argument("test-id", type=str, help="Pass a test id")
    args = parser.parse_args()

    if args.command == "get-test-ids":
        print(get_test_ids())
    elif args.command == "get-test-path":
        print(get_test_path(vars(args)["test-id"]))
