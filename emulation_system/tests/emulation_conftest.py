"""Constants for comparison in tests."""
from emulation_system.commands.command import CommandList, Command
from emulation_system.commands.emulation_command_creator import (
    AbstractEmulationCommandCreator,
)
from tests.conftest import (
    TEST_CONF_MODULES_EXPECTED_COMMIT,
    TEST_CONF_OPENTRONS_EXPECTED_COMMIT,
    TEST_CONF_FIRMWARE_PATH,
    TEST_CONF_MODULES_PATH,
    TEST_CONF_OPENTRONS_PATH,
    TEST_CONF_FIRMWARE_HEAD,
    TEST_CONF_MODULES_HEAD,
    TEST_CONF_OPENTRONS_HEAD,
    TEST_CONF_FIRMWARE_EXPECTED_COMMIT,
)

MADE_UP_MODULES_PATH = "/these/are/not/the/modules/you/are/looking/for"
MADE_UP_OPENTRONS_PATH = "/otie/I/am/your/father"
MADE_UP_FIRMWARE_PATH = "/the/force/is/strong/with/this/firmware"

MADE_UP_MODULES_SHA = "modulessha"
MADE_UP_OPENTRONS_SHA = "opentrons"
MADE_UP_FIRMWARE_SHA = "firmwaresha"


EXPECTED_FIRMWARE_COMMIT = TEST_CONF_FIRMWARE_EXPECTED_COMMIT.replace(
    "{{commit-sha}}", MADE_UP_FIRMWARE_SHA
)
EXPECTED_MODULES_COMMIT = TEST_CONF_MODULES_EXPECTED_COMMIT.replace(
    "{{commit-sha}}", MADE_UP_MODULES_SHA
)
EXPECTED_OPENTRONS_COMMIT = TEST_CONF_OPENTRONS_EXPECTED_COMMIT.replace(
    "{{commit-sha}}", MADE_UP_OPENTRONS_SHA
)

BASIC_DEV_CMDS_TO_RUN = CommandList(
    [
        Command(
            command_name=AbstractEmulationCommandCreator.KILL_COMMAND_NAME,
            command="docker-compose -f docker-compose-dev.yaml kill",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
        Command(
            command_name=AbstractEmulationCommandCreator.REMOVE_COMMAND_NAME,
            command="docker-compose -f docker-compose-dev.yaml rm -f",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
        Command(
            command_name=AbstractEmulationCommandCreator.BUILD_COMMAND_NAME,
            command="docker-compose -f docker-compose-dev.yaml build",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
            env={
                "COMPOSE_DOCKER_CLI_BUILD": "1",
                "DOCKER_BUILDKIT": "1",
                "OT3_FIRMWARE_DIRECTORY": TEST_CONF_FIRMWARE_PATH,
                "OPENTRONS_MODULES_DIRECTORY": TEST_CONF_MODULES_PATH,
                "OPENTRONS_DIRECTORY": TEST_CONF_OPENTRONS_PATH,
            },
        ),
        Command(
            command_name=AbstractEmulationCommandCreator.RUN_COMMAND_NAME,
            command="docker-compose -f docker-compose-dev.yaml up",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
            env={
                "OT3_FIRMWARE_DIRECTORY": TEST_CONF_FIRMWARE_PATH,
                "OPENTRONS_MODULES_DIRECTORY": TEST_CONF_MODULES_PATH,
                "OPENTRONS_DIRECTORY": TEST_CONF_OPENTRONS_PATH,
            },
        ),
    ]
)

COMPLEX_DEV_COMMANDS_TO_RUN = CommandList(
    [
        Command(
            command_name=AbstractEmulationCommandCreator.KILL_COMMAND_NAME,
            command="docker-compose -f docker-compose-dev.yaml kill",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
        Command(
            command_name=AbstractEmulationCommandCreator.REMOVE_COMMAND_NAME,
            command="docker-compose -f docker-compose-dev.yaml rm -f",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
        Command(
            command_name=AbstractEmulationCommandCreator.BUILD_COMMAND_NAME,
            command="docker-compose -f docker-compose-dev.yaml build",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
            env={
                "COMPOSE_DOCKER_CLI_BUILD": "1",
                "DOCKER_BUILDKIT": "1",
                "OT3_FIRMWARE_DIRECTORY": MADE_UP_FIRMWARE_PATH,
                "OPENTRONS_MODULES_DIRECTORY": MADE_UP_MODULES_PATH,
                "OPENTRONS_DIRECTORY": MADE_UP_OPENTRONS_PATH,
            },
        ),
        Command(
            AbstractEmulationCommandCreator.RUN_COMMAND_NAME,
            command="docker-compose -f docker-compose-dev.yaml up -d",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
            env={
                "OT3_FIRMWARE_DIRECTORY": MADE_UP_FIRMWARE_PATH,
                "OPENTRONS_MODULES_DIRECTORY": MADE_UP_MODULES_PATH,
                "OPENTRONS_DIRECTORY": MADE_UP_OPENTRONS_PATH,
            },
        ),
    ]
)

BASIC_PROD_COMMANDS_TO_RUN = CommandList(
    [
        Command(
            command_name=AbstractEmulationCommandCreator.KILL_COMMAND_NAME,
            command="docker-compose -f docker-compose.yaml kill",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
        Command(
            command_name=AbstractEmulationCommandCreator.REMOVE_COMMAND_NAME,
            command="docker-compose -f docker-compose.yaml rm -f",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
        Command(
            AbstractEmulationCommandCreator.BUILD_COMMAND_NAME,
            (
                "docker-compose -f docker-compose.yaml build "
                f"--build-arg FIRMWARE_SOURCE_DOWNLOAD_LOCATION="
                f"{TEST_CONF_FIRMWARE_HEAD} "
                f"--build-arg MODULE_SOURCE_DOWNLOAD_LOCATION="
                f"{TEST_CONF_MODULES_HEAD} "
                f"--build-arg OPENTRONS_SOURCE_DOWNLOAD_LOCATION="
                f"{TEST_CONF_OPENTRONS_HEAD} "
            ),
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
            env=AbstractEmulationCommandCreator.DOCKER_BUILD_ENV_VARS,
        ),
        Command(
            AbstractEmulationCommandCreator.RUN_COMMAND_NAME,
            "docker-compose -f docker-compose.yaml up",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
    ]
)

COMPLEX_PROD_COMMANDS_TO_RUN = CommandList(
    [
        Command(
            command_name=AbstractEmulationCommandCreator.KILL_COMMAND_NAME,
            command="docker-compose -f docker-compose.yaml kill",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
        Command(
            command_name=AbstractEmulationCommandCreator.REMOVE_COMMAND_NAME,
            command="docker-compose -f docker-compose.yaml rm -f",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
        Command(
            AbstractEmulationCommandCreator.BUILD_COMMAND_NAME,
            (
                "docker-compose -f docker-compose.yaml build "
                f"--build-arg FIRMWARE_SOURCE_DOWNLOAD_LOCATION="
                f"{EXPECTED_FIRMWARE_COMMIT} "
                f"--build-arg MODULE_SOURCE_DOWNLOAD_LOCATION="
                f"{EXPECTED_MODULES_COMMIT} "
                f"--build-arg OPENTRONS_SOURCE_DOWNLOAD_LOCATION="
                f"{EXPECTED_OPENTRONS_COMMIT} "
            ),
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
            env=AbstractEmulationCommandCreator.DOCKER_BUILD_ENV_VARS,
        ),
        Command(
            AbstractEmulationCommandCreator.RUN_COMMAND_NAME,
            "docker-compose -f docker-compose.yaml up -d",
            cwd=AbstractEmulationCommandCreator.DOCKER_RESOURCES_LOCATION,
        ),
    ]
)
