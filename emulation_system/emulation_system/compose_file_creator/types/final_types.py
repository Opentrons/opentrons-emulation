"""Types to cast to in order to convert to Docker Compose File.

These types should only be used at the very end of building the compose file,
(when building a Service).
Do not use these types when implementing business logic, they suck, and it makes
mypy hate everything you have ever done.
"""

from typing import List, TypeAlias

from .. import BuildItem
from ..output.compose_file_model import (
    DependsOn,
    Healthcheck,
    ListOrDict,
    Port,
    Volume1,
)

# TODO: Need to figure out what to do with DependsOn and Networks
#       In compose_file_model.py they implement constr which mypy does not like.

ServiceVolumes: TypeAlias = List[str | Volume1] | None
ServicePorts: TypeAlias = List[float | str | Port] | None
ServiceEnvironment: TypeAlias = ListOrDict | None
ServiceContainerName: TypeAlias = str | None
ServiceImage: TypeAlias = str | None
ServiceBuild: TypeAlias = str | BuildItem | None
ServiceTTY: TypeAlias = bool | None
ServiceCommand: TypeAlias = str | List[str] | None
ServiceHealthcheck: TypeAlias = Healthcheck
ServiceDependsOn: TypeAlias = dict[str, DependsOn] | None
