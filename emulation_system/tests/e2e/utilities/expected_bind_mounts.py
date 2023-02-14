"""Helper class containing expected bind mounts for e2e test."""

from dataclasses import dataclass
from typing import Optional

from tests.e2e.utilities.consts import ExpectedMount


@dataclass
class ExpectedBindMounts:
    """Helper class containing expected bind mounts for e2e test."""

    MONOREPO: Optional[ExpectedMount]
    FIRMWARE: Optional[ExpectedMount]
    MODULES: Optional[ExpectedMount]
