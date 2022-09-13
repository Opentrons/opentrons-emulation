"""Types to cast to in order to convert to Docker Compose File.

These types should only be used at the very end of building the compose file,
(when building a Service).
Do not use these types when implementing business logic, they suck, and it makes
mypy hate everything you have ever done.
"""

from typing import List, Optional, Union

from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    ListOrDict,
    Port,
    Volume1,
)

ServiceVolumes = Optional[List[Union[str, Volume1]]]
ServicePorts = Optional[List[Union[float, str, Port]]]
ServiceEnvironment = Optional[ListOrDict]
ServiceContainerName = Optional[str]
ServiceImage = Optional[str]
ServiceBuild = Optional[Union[str, BuildItem]]
ServiceTTY = Optional[bool]
ServiceCommand = Optional[Union[str, List[str]]]

# TODO: Need to figure out what to do with DependsOn and Networks
#       In compose_file_model.py they implement constr which mypy does not like.
