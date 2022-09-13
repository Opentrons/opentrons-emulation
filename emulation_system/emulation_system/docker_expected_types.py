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
