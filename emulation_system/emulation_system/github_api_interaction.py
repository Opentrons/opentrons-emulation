"""This module contains functions for interacting with the GitHub API."""

import os
from typing import Dict

import requests


def _get_github_auth_headers() -> Dict[str, str] | None:
    """Returns the GitHub auth headers if the GITHUB_TOKEN environment variable is set.

    This is so we get rate limited at 1000 requests per hour instead of 60.
    This will only be used by e2e testing. Unit tests are patched.
    """
    if os.environ.get("GITHUB_TOKEN") is not None:
        return {"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"}
    else:
        return None


HEADERS = _get_github_auth_headers()


def github_api_is_up() -> bool:
    """Checks if the GitHub API is up and running.

    Returns:
        bool: True if the GitHub API is up and running, False otherwise.
    """
    api_not_available = False
    try:
        response = requests.get("https://api.github.com", headers=HEADERS)
        if response.status_code != 200:
            api_not_available = True
    except requests.exceptions.ConnectionError:
        api_not_available = True

    if api_not_available:
        raise ConnectionError("GitHub API is not available.")
    else:
        return True


def check_if_ref_exists(owner: str, repo: str, ref: str) -> bool:
    """Checks if a ref exists in a given repo."""
    github_api_is_up()
    branch_response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{ref}",
        headers=HEADERS,
    ).status_code
    tag_response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/git/ref/tags/{ref}",
        headers=HEADERS,
    ).status_code

    if 200 in (branch_response, tag_response):
        return True
    else:
        return False
