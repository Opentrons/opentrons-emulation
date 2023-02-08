from dataclasses import dataclass
from typing import List

from docker.models.containers import Container

from tests.e2e.utilities.consts import ExpectedMount, ExpectedNamedVolume


@dataclass
class TestDescription:
    desc: str

    @classmethod
    def from_named_volume(
        cls,
        container: Container,
        named_volume: ExpectedNamedVolume,
        confirm_not_exists: bool = False,
    ) -> "TestDescription":
        expectation = "does not have" if confirm_not_exists else "has"
        return cls(
            desc=f'Confirming container "{container.name}" {expectation} named volume '
            f'"{named_volume.VOLUME_NAME}" with path '
            f'"{named_volume.DEST_PATH}"'
        )

    @classmethod
    def from_mount(
        cls,
        container: Container,
        mount: ExpectedMount,
        confirm_not_exists: bool = False,
    ) -> "TestDescription":
        expectation = "does not have" if confirm_not_exists else "has"
        return cls(
            desc=(
                f'Confirming container "{container.name}" {expectation} has mount with path '
                f'"{mount.SOURCE_PATH}:{mount.DEST_PATH}"'
            )
        )

    def generate_pass_message(self) -> str:
        return f"PASS: {self.desc}"

    def generate_fail_message(self) -> str:
        return f"FAIL: {self.desc}"


MONOREPO_BUILDER_CREATED = TestDescription(
    desc="Confirming monorepo builder was created",
)

MONOREPO_BUILDER_NOT_CREATED = TestDescription(
    desc="Confirming monorepo builder was not created",
)

OT3_FIRMWARE_BUILDER_CREATED = TestDescription(
    desc="Confirming ot3-firmware builder was created",
)

OT3_FIRMWARE_BUILDER_NOT_CREATED = TestDescription(
    desc="Confirming ot3-firmware builder was not created",
)

OPENTRONS_MODULES_BUILDER_CREATED = TestDescription(
    desc="Confirming opentrons-modules builder was created",
)

OPENTRONS_MODULES_BUILDER_NOT_CREATED = TestDescription(
    desc="Confirming opentrons-modules builder was not created",
)

MONOREPO_SOURCE_MOUNTED = TestDescription(
    desc="Confirming monorepo builder has local source mounted",
)

MONOREPO_SOURCE_NOT_MOUNTED = TestDescription(
    desc="Confirming monorepo builder does not have local source mounted",
)

OT3_FIRMWARE_SOURCE_MOUNTED = TestDescription(
    desc="Confirming ot3-firmware builder has local source mounted",
)

OT3_FIRMWARE_SOURCE_NOT_MOUNTED = TestDescription(
    desc="Confirming ot3-firmware builder does not have local source mounted",
)

OPENTRONS_MODULES_SOURCE_MOUNTED = TestDescription(
    desc="Confirming opentrons-modules builder has local source mounted",
)

OPENTRONS_MODULES_SOURCE_NOT_MOUNTED = TestDescription(
    desc="Confirming opentrons-modules builder does not have local source mounted",
)


class E2ETestOutput:
    def __init__(self) -> None:
        self._output: List[str] = []
        self._failure = False
        self._failure_count = 0

    def append_result(self, assertion: bool, result: TestDescription) -> None:
        if assertion:
            self._output.append(result.generate_pass_message())
        else:
            self._failure = True
            self._failure_count += 1
            self._output.append(result.generate_fail_message())

    def get_results(self) -> str:
        return "\n" + "\n".join(self._output)

    @property
    def is_failure(self) -> bool:
        return self._failure

    @property
    def failure_count(self) -> int:
        return self._failure_count
