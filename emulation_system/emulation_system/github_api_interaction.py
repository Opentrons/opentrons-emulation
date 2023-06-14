"""This module contains functions for interacting with the GitHub API."""

import requests

from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
)


def github_api_is_up() -> bool:
    """Checks if the GitHub API is up and running.

    Returns:
        bool: True if the GitHub API is up and running, False otherwise.
    """
    try:
        response = requests.get("https://api.github.com")
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False


def check_if_branch_exists(repo: OpentronsRepository, branch: str) -> bool:
    """Checks if a branch exists in a given repo.

    Args:
        repo (str): The name of the repo to check.
        branch (str): The name of the branch to check.

    Returns:
        bool: True if the branch exists, False otherwise.
    """
    response = requests.get(
        f"https://api.github.com/repos/Opentrons/{repo.value}/branches/{branch}"
    )
    if response.status_code == 200:
        return True
    else:
        return False
