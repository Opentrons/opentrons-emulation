from typing import (
    List,
    Optional,
)

from emulation_system.compose_file_creator.errors import (
    HardwareDoesNotExistError,
    IncorrectHardwareError,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    Hardware,
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import CANServerImages
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from .abstract_service_builder import AbstractServiceBuilder
from ...intermediate_types import (
    Command,
    DependsOn,
    EnvironmentVariables,
    Ports,
    RequiredNetworks,
    Volumes,
)
from ...service_creation.shared_functions import (
    add_opentrons_named_volumes,
    generate_container_name,
    get_build_args,
    get_entrypoint_mount_string,
    get_service_build,
)


class ConcreteCANServerServiceBuilder(AbstractServiceBuilder):

    CAN_SERVER_NAME = "can-server"
    NO_BUILD_ARGS_REASON = 'can-server-source-type is "local"'
    BUILD_ARGS_REASON = 'can-server-source-type is "remote"'

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        super().__init__(config_model, global_settings)
        self._dev = dev
        self._ot3 = self._get_ot3(config_model)
        self._image = self._generate_image()

    @staticmethod
    def _get_ot3(config_model: SystemConfigurationModel):
        ot3 = config_model.robot
        if ot3 is None:
            raise HardwareDoesNotExistError(Hardware.OT3)
        if ot3.hardware != Hardware.OT3:
            raise IncorrectHardwareError(ot3.hardware, Hardware.OT3)

        return ot3

    def _generate_image(self) -> str:
        source_type = self._ot3.can_server_source_type
        image_name = (
            CANServerImages().local_firmware_image_name
            if source_type == SourceType.LOCAL
            else CANServerImages().remote_firmware_image_name
        )

        return image_name

    @staticmethod
    def _log_mounts(mounts: List[str]) -> None:
        ...

    @staticmethod
    def _log_volumes(volumes: List[str]) -> None:
        ...

    def generate_container_name(self) -> str:
        can_server_name = generate_container_name(
            self.CAN_SERVER_NAME, self._config_model
        )
        return can_server_name

    def generate_image(self) -> str:
        return self._image

    def is_tty(self) -> bool:
        tty = True
        return tty

    def generate_networks(self) -> RequiredNetworks:
        networks = self._config_model.required_networks
        return networks

    def generate_build(self) -> Optional[BuildItem]:
        repo = OpentronsRepository.OPENTRONS
        source_type = self._ot3.can_server_source_type
        if source_type == SourceType.REMOTE:
            build_args = get_build_args(
                repo,
                self._ot3.can_server_source_location,
                self._global_settings.get_repo_commit(repo),
                self._global_settings.get_repo_head(repo),
            )
            why = self.BUILD_ARGS_REASON

        else:
            build_args = None
            why = self.NO_BUILD_ARGS_REASON
        return get_service_build(self._image, build_args, self._dev)

    def generate_volumes(self) -> Optional[Volumes]:
        if self._ot3.can_server_source_type == SourceType.LOCAL:
            mounts = [get_entrypoint_mount_string()]
            mounts.extend(self._ot3.get_can_mount_strings())
            add_opentrons_named_volumes(mounts)
        else:
            mounts = None

        return mounts

    def generate_command(self) -> Optional[Command]:
        return None

    def generate_ports(self) -> Optional[Ports]:
        return self._ot3.get_can_server_bound_port()

    def generate_depends_on(self) -> Optional[DependsOn]:
        return None

    def generate_env_vars(self) -> Optional[EnvironmentVariables]:
        return None
