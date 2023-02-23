"""Class for capturing output of single test."""

from dataclasses import dataclass

from docker.models.containers import Container  # type: ignore[import]

from tests.e2e.utilities.consts import ExpectedMount, ExpectedNamedVolume


@dataclass
class TestDescription:
    """Class representing description of test result."""

    desc: str

    @classmethod
    def from_named_volume(
        cls,
        container: Container,
        named_volume: ExpectedNamedVolume,
        confirm_not_exists: bool = False,
    ) -> "TestDescription":
        """Helper method to generate TestDescrition from a ExpectedNamedVolume object"""
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
        """Helper method to genreate TestDescription object from ExpectedMount object"""
        expectation = "does not have" if confirm_not_exists else "has"
        return cls(
            desc=(
                f'Confirming container "{container.name}" {expectation} has mount with path '
                f'"{mount.SOURCE_PATH}:{mount.DEST_PATH}"'
            )
        )

    def generate_pass_message(self) -> str:
        """Call this method if test passes."""
        return f"PASS: {self.desc}"

    def generate_fail_message(self) -> str:
        """Call this method if test fails."""
        return f"FAIL: {self.desc}"
