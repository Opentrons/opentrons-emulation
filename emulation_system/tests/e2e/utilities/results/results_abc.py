from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition


@dataclass
class ResultABC(ABC):
    @classmethod
    @abstractmethod
    def get_expected_results(
        cls: Type["ResultABC"], system_test_def: SystemTestDefinition
    ) -> "ResultABC":
        ...

    @classmethod
    @abstractmethod
    def get_actual_results(
        cls: Type["ResultABC"], system_under_test: E2EHostSystem
    ) -> "ResultABC":
        ...



@dataclass
class ModuleResultABC(ResultABC):

    @classmethod
    @abstractmethod
    def NO_MODULES_EXPECTED_RESULT(cls) -> "ModuleResultABC":
        raise NotImplemented
