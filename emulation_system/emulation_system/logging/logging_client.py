from typing import Optional

from emulation_system.compose_file_creator.conversion.intermediate_types import RequiredNetworks
from emulation_system.compose_file_creator.output.compose_file_model import ListOrDict
from emulation_system.logging.console import logging_console


class LoggingClient:

    def __init__(self) -> None:
        ...

    @staticmethod
    def log_header(service_being_built: str) -> None:
        logging_console.header_print(f"Creating Service for {service_being_built}")

    @staticmethod
    def log_container_name(
        container_name: str, system_unique_id: Optional[str]
    ) -> None:
        if system_unique_id is None:
            message = (
                '"system-unique-id" is None. \n'
                f'Setting container_name as passed to: "{container_name}"'
            )
        else:
            message = []
            message.append(f'"system-unique-id" is "{system_unique_id}".')
            message.append(f'Prepending it to passed container name. ')
            message.append(f'Setting container name to "{container_name}"')

        logging_console.tabbed_header_print('container_name')
        logging_console.double_tabbed_print(*message)

    @staticmethod
    def log_image_name(image_name: str, source_type: str) -> None:
        logging_console.tabbed_header_print('image')
        logging_console.double_tabbed_print(
            f'Using image name "{image_name}" since '
            f'can-server-source-type is "{source_type}"'
        )

    @staticmethod
    def log_networks(networks: RequiredNetworks) -> None:
        tabbed_networks = ['\t"' + network + '"' for network in networks]
        logging_console.tabbed_header_print('networks')
        logging_console.double_tabbed_print(
            "Adding the following networks:",
            *tabbed_networks
        )

    @staticmethod
    def log_tty(is_tty: bool) -> None:
        if is_tty:
            val = "true"
        else:
            val = "false"
        logging_console.tabbed_header_print('tty')
        logging_console.double_tabbed_print(f'Setting "tty" to "{val}"')

    @staticmethod
    def log_build(build_args: Optional[ListOrDict], why: str) -> None:
        if build_args is None:
            output = [f"Adding no build args since {why}"]
        else:
            output = [
                f"Since {why}, Adding the following build args:",
                f"\t{build_args.dict()['__root__']}"
            ]
        logging_console.tabbed_header_print("build.args")
        logging_console.double_tabbed_print(*output)
