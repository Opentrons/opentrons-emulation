"""Class for capturing output from all tests."""

from typing import List

from tests.e2e.utilities.results.single_test_description import TestDescription


class E2ETestOutput:
    """Class containing all results from e2e test being ran."""

    def __init__(self) -> None:
        self._output: List[str] = []
        self._failure = False
        self._failure_count = 0

    def append_result(self, assertion: bool, result: TestDescription) -> None:
        """Add a result to test output."""
        if assertion:
            self._output.append(result.generate_pass_message())
        else:
            self._failure = True
            self._failure_count += 1
            self._output.append(result.generate_fail_message())

    def get_results(self) -> str:
        """Return formatted results."""
        return "\n" + "\n".join(self._output)

    @property
    def is_failure(self) -> bool:
        """Whether test failed."""
        return self._failure

    @property
    def failure_count(self) -> int:
        """Number of failures."""
        return self._failure_count
