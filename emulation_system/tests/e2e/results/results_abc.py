"""ABC for all e2e testing results"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition


@dataclass
class ResultABC(ABC):
    """ABC for all e2e testing results.

    Requires classes extending it to define methods, get_expected_results and get_actual_results.
    """

    @classmethod
    @abstractmethod
    def get_expected_results(
        cls: Type["ResultABC"], system_test_def: SystemTestDefinition
    ) -> "ResultABC":
        """Returns instance of class containing expected results for the test."""
        ...

    @classmethod
    @abstractmethod
    def get_actual_results(
        cls: Type["ResultABC"], system_under_test: E2EHostSystem
    ) -> "ResultABC":
        """Returns instance of class containing actual results for the test."""
        ...


@dataclass
class ModuleResultABC(ResultABC):
    """ABC for module results.

    Requires classes extending it to define what no modules look like.
    """

    @classmethod
    @abstractmethod
    def NO_MODULES_EXPECTED_RESULT(cls) -> "ModuleResultABC":
        """Requires user to define what no modules look like for the result.

        This keeps all module results in the same place for reference.
        """
        raise NotImplementedError
