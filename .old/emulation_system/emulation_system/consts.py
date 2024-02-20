"""System-wide constants."""

from __future__ import annotations

import os

# Latest Git Commit
LATEST_KEYWORD = "latest"

# Root of repo
ROOT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
)

# PORTS
ROBOT_SERVER_DEFAULT_PORT = 31950
OT3_STATE_MANAGER_BOUND_PORT = 9999

# FILE NAMES
DEFAULT_ENTRYPOINT_NAME = "entrypoint.sh"
LOCAL_OT3_FIRMWARE_BUILDER_SCRIPT_NAME = "ot3_firmware_builder.sh"

DEFAULT_CONFIGURATION_FILE_PATH = f"{ROOT_DIR}/configuration.json"
PIPETTE_VERSIONS_FILE_PATH = f"{ROOT_DIR}/pipette_versions.json"
CONFIGURATION_FILE_LOCATION_VAR_NAME = "CONFIGURATION_FILE_LOCATION"
DOCKERFILE_DIR_LOCATION = f"{ROOT_DIR}/docker/"
ENTRYPOINT_FILE_LOCATION = f"{DOCKERFILE_DIR_LOCATION}{DEFAULT_ENTRYPOINT_NAME}"

LOCAL_OT3_FIRMWARE_BUILDER_SCRIPT_PATH = (
    f"{DOCKERFILE_DIR_LOCATION}entrypoints/{LOCAL_OT3_FIRMWARE_BUILDER_SCRIPT_NAME}"
)
DOCKERFILE_NAME = "Dockerfile"
DEV_DOCKERFILE_NAME = "dev_Dockerfile"
ROOM_TEMPERATURE: float = 23.0
DEFAULT_DOCKER_COMPOSE_VERSION = "3.8"
DEFAULT_NETWORK_NAME = "local-network"
COMMIT_SHA_REGEX = r"^[0-9a-f]{40}"

EEPROM_FILE_NAME = "eeprom.bin"

MONOREPO_NAMED_VOLUME_STRING = "monorepo-wheels:/dist"

OT3_FIRMWARE_BUILDER_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING = (
    "state-manager-dist:/volumes/state-manager-dist"
)
EMULATOR_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING = (
    "state-manager-dist:/state-manager-dist"
)

OT3_FIRMWARE_BUILDER_STATE_MANAGER_VENV_NAMED_VOLUME_STRING = (
    "state-manager-venv:/volumes/state-manager-venv"
)
EMULATOR_STATE_MANAGER_VENV_NAMED_VOLUME_STRING = "state-manager-venv:/.venv"

OT3_FIRMWARE_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME = (
    "ot3-firmware-build-host-docker-cache:/ot3-firmware/build-host"
)
OT3_FIRMWARE_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME = (
    "ot3-firmware-stm32-tools-docker-cache:/ot3-firmware/stm32-tools"
)

OPENTRONS_MODULES_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME = (
    "opentrons-modules-build-host-docker-cache:/opentrons-modules/build-host"
)
OPENTRONS_MODULES_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME = (
    "opentrons-modules-stm32-tools-docker-cache:/opentrons-modules/stm32-tools"
)
