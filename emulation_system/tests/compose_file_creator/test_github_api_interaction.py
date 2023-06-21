"""Validate github API interface"""

import pytest

from emulation_system import github_api_interaction


@pytest.mark.parametrize(
    "owner, repo, ref, exists",
    [
        ("Opentrons", "opentrons", "edge", True),
        ("Opentrons", "opentrons", "ot3@0.8.0-alpha.2", True),
        ("Opentrons", "opentrons", "main", False),
        ("Opentrons", "opentrons-modules", "edge", True),
        ("Opentrons", "opentrons-modules", "heater-shaker@v1.0.3", True),
        ("Opentrons", "opentrons-modules", "main", False),
        ("Opentrons", "ot3-firmware", "main", True),
        ("Opentrons", "ot3-firmware", "v14", True),
        ("Opentrons", "ot3-firmware", "edge", False),
    ],
)
def test_check_if_ref_exists(owner: str, repo: str, ref: str, exists: bool) -> None:
    """Test check_if_ref_exists."""
    assert github_api_interaction.check_if_ref_exists(owner, repo, ref) == exists
