from dataclasses import dataclass
from typing import Optional

from tests.e2e.utilities.consts import ExpectedMount


@dataclass
class ExpectedBindMounts:
    MONOREPO: Optional[ExpectedMount]
    FIRMWARE: Optional[ExpectedMount]
    MODULES: Optional[ExpectedMount]
