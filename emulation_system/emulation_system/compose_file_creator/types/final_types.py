"""Types to cast to in order to convert to Docker Compose File.

These types should only be used at the very end of building the compose file,
(when building a Service).
Do not use these types when implementing business logic, they suck, and it makes
mypy hate everything you have ever done.
"""

from typing import List, Optional, Union

from .. import BuildItem
from ..output.compose_file_model import ListOrDict, Port, Volume1

# TODO: Need to figure out what to do with DependsOn and Networks
#       In compose_file_model.py they implement constr which mypy does not like.


ServiceVolumes = Optional[List[Union[str, Volume1]]]
ServicePorts = Optional[List[Union[float, str, Port]]]
ServiceEnvironment = Optional[ListOrDict]
ServiceContainerName = Optional[str]
ServiceImage = Optional[str]
ServiceBuild = Optional[Union[str, BuildItem]]
ServiceTTY = Optional[bool]
ServiceCommand = Optional[Union[str, List[str]]]
