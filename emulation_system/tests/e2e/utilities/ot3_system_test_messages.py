from dataclasses import dataclass
from typing import List


@dataclass
class TestResult:

    desc: str

    def generate_pass_message(self) -> str:
        return f"PASS: {self.desc}"

    def generate_fail_message(self) -> str:
        return f"FAIL: {self.desc}"


MONOREPO_BUILDER_CREATED = TestResult(
    desc="Confirming monorepo builder was created",
)

MONOREPO_BUILDER_NOT_CREATED = TestResult(
    desc="Confirming monorepo builder was not created",
)

OT3_FIRMWARE_BUILDER_CREATED = TestResult(
    desc="Confirming ot3-firmware builder was created",
)

OT3_FIRMWARE_BUILDER_NOT_CREATED = TestResult(
    desc="Confirming ot3-firmware builder was not created",
)

OPENTRONS_MODULES_BUILDER_CREATED = TestResult(
    desc="Confirming opentrons-modules builder was created",
)

OPENTRONS_MODULES_BUILDER_NOT_CREATED = TestResult(
    desc="Confirming opentrons-modules builder was not created",
)

MONOREPO_SOURCE_MOUNTED = TestResult(
    desc="Confirming monorepo builder has local source mounted",
)

MONOREPO_SOURCE_NOT_MOUNTED = TestResult(
    desc="Confirming monorepo builder does not have local source mounted",
)

OT3_FIRMWARE_SOURCE_MOUNTED = TestResult(
    desc="Confirming ot3-firmware builder has local source mounted",
)

OT3_FIRMWARE_SOURCE_NOT_MOUNTED = TestResult(
    desc="Confirming ot3-firmware builder does not have local source mounted",
)

OPENTRONS_MODULES_SOURCE_MOUNTED = TestResult(
    desc="Confirming opentrons-modules builder has local source mounted",
)

OPENTRONS_MODULES_SOURCE_NOT_MOUNTED = TestResult(
    desc="Confirming opentrons-modules builder does not have local source mounted",
)


class E2ETestOutput:
    def __init__(self) -> None:
        self._output: List[str] = []
        self._failure = False
        self._failure_count = 0

    def append_result(
        self,
        assertion: bool,
        result: TestResult
    ) -> None:
        if assertion:
            self._output.append(result.generate_pass_message())
        else:
            self._failure = True
            self._failure_count += 1
            self._output.append(result.generate_fail_message())

    def get_results(self) -> str:
        return "\n" + '\n'.join(self._output)

    @property
    def is_failure(self) -> bool:
        return self._failure

    @property
    def failure_count(self) -> int:
        return self._failure_count
