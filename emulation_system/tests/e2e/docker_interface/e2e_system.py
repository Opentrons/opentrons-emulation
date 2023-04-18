from dataclasses import dataclass

from .expected_bind_mounts import ExpectedBindMounts
from .module_containers import ModuleContainers
from .ot3_containers import OT3SystemUnderTest


@dataclass
class E2EHostSystem:
    ot3_containers: OT3SystemUnderTest
    module_containers: ModuleContainers
    expected_binds_mounts: ExpectedBindMounts
