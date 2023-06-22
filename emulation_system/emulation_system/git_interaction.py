"""This module contains functions for interacting with git."""

import subprocess
from functools import lru_cache
from typing import List


def check_if_ref_exists(owner: str, repo: str, ref: str) -> bool:
    """Checks if a ref exists in a given repo."""
    remote_url = f"https://github.com/{owner}/{repo}.git"
    return ref in get_valid_ref_list(remote_url)


# lru_cache is not useful for the actual end user
# of opentrons-emulation since the cache is only maintained
# for the lifetime of the python executable. Whenever the user
# calls a make command, the python executable is re-run.

# However, it is still useful for tests since those are all run in the
# same python executable. This prevents the need to make a network call for every test
# that uses this function, which is almost all of them.

# Although we could possibly run into a situation where refs have been updated
# since the python executable was started, this doesn't really matter for tests
# since the refs we are checking for are hardcoded to old refs.

# This changes test execution from ~80 seconds to ~20 seconds.
@lru_cache
def get_valid_ref_list(remote_url: str) -> List[str]:
    """Gets a sorted list of valid refs from a remote URL."""

    def _format_line(line: str) -> str:
        """Formats a line from the output of git ls-remote into a valid ref."""
        sha_removed = line.split("\t")[1]
        tags_path_removed = sha_removed.replace("refs/tags/", "")
        heads_path_removed = tags_path_removed.replace("refs/heads/", "")
        weird_tag_thing_removed = heads_path_removed.replace("^{}", "")
        return weird_tag_thing_removed

    try:
        output = subprocess.run(
            ["git", "ls-remote", "--tags", "--heads", remote_url],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Unable to get valid ref list from {remote_url}. " f"Error: {e.stderr}"
        )
    formatted_refs = [_format_line(item) for item in output.split("\n")]
    return sorted(list(set(formatted_refs)))
