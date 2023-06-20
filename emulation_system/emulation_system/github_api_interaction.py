"""This module contains functions for interacting with the GitHub API."""

import requests


def github_api_is_up() -> bool:
    """Checks if the GitHub API is up and running.

    Returns:
        bool: True if the GitHub API is up and running, False otherwise.
    """
    api_not_available = False
    try:
        response = requests.get("https://api.github.com")
        if response.status_code != 200:
            api_not_available = True
    except requests.exceptions.ConnectionError:
        api_not_available = True

    if api_not_available:
        raise ConnectionError("GitHub API is not available.")
    else:
        return True


def check_if_branch_exists(owner: str, repo: str, branch: str) -> bool:
    """Checks if a branch exists in a given repo."""
    github_api_is_up()
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    )
    if response.status_code == 200:
        return True
    else:
        return False
