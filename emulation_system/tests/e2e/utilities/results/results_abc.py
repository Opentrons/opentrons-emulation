from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Type,
    TypeVar,
)

from tests.e2e.fixtures.e2e_system import E2EHostSystem
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition

TResults = TypeVar("TResults")

@dataclass
class ResultsABC(ABC):

    @classmethod
    @abstractmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        ...

    @classmethod
    @abstractmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        ...
