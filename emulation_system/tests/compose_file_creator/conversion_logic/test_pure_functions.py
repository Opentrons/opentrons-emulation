"""Tests for conversion pure functions."""

from typing import (
    List,
    Optional,
    Type,
)

import pytest

from emulation_system.compose_file_creator.conversion.service_creation.shared_functions import (  # noqa: E501
    get_build_args,
    get_service_build,
)

from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    ListOrDict,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.consts import DOCKERFILE_DIR_LOCATION


@pytest.mark.parametrize(
    "source_repo,source_location,format_string,head,expected_value",
    [
        [
            OpentronsRepository.OPENTRONS,
            "ca82a6dff817ec66f44342007202690a93763949",
            "https://github.com/Opentrons/opentrons/archive/{{commit-sha}}.zip",
            "https://github.com/Opentrons/opentrons/archive/refs/heads/edge.zip",
            ListOrDict(
                __root__={
                    "OPENTRONS_SOURCE_DOWNLOAD_LOCATION": "https://github.com/"
                    "Opentrons/opentrons/archive/"
                    "ca82a6dff817ec66f44342"
                    "007202690a93763949.zip"
                }
            ),
        ],
        [
            OpentronsRepository.OPENTRONS_MODULES,
            "ca82a6dff817ec66f44342007202690a93763949",
            "https://github.com/Opentrons/opentrons-modules/archive/{{commit-sha}}.zip",
            "https://github.com/Opentrons/opentrons/archive/refs/heads/edge.zip",
            ListOrDict(
                __root__={
                    "MODULE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/"
                    "opentrons-modules/archive/"
                    "ca82a6dff817ec66f4434200720269"
                    "0a93763949.zip"
                }
            ),
        ],
        [
            OpentronsRepository.OT3_FIRMWARE,
            "ca82a6dff817ec66f44342007202690a93763949",
            "https://github.com/Opentrons/ot3-firmware/archive/{{commit-sha}}.zip",
            "https://github.com/Opentrons/opentrons/archive/refs/heads/edge.zip",
            ListOrDict(
                __root__={
                    "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/"
                    "Opentrons/ot3-firmware/"
                    "archive/ca82a6dff817ec66f443"
                    "42007202690a93763949.zip"
                }
            ),
        ],
        [
            OpentronsRepository.OPENTRONS,
            "latest",
            "https://github.com/Opentrons/opentrons/archive/{{commit-sha}}.zip",
            "https://github.com/Opentrons/opentrons/archive/refs/heads/edge.zip",
            ListOrDict(
                __root__={
                    "OPENTRONS_SOURCE_DOWNLOAD_LOCATION": "https://github.com/"
                    "Opentrons/opentrons/archive/"
                    "refs/heads/edge.zip"
                }
            ),
        ],
        [
            OpentronsRepository.OPENTRONS_MODULES,
            "latest",
            "https://github.com/Opentrons/opentrons-modules/archive/{{commit-sha}}.zip",
            "https://github.com/Opentrons/opentrons-modules/archive/refs/heads/edge.zip",
            ListOrDict(
                __root__={
                    "MODULE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/"
                    "opentrons-modules/archive/refs/"
                    "heads/edge.zip"
                }
            ),
        ],
        [
            OpentronsRepository.OT3_FIRMWARE,
            "latest",
            "https://github.com/Opentrons/ot3-firmware/archive/{{commit-sha}}.zip",
            "https://github.com/Opentrons/ot3-firmware/archive/refs/heads/main.zip",
            ListOrDict(
                __root__={
                    "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/"
                    "ot3-firmware/archive/refs/"
                    "heads/main.zip"
                }
            ),
        ],
    ],
)
def test_get_build_args(
    source_repo: OpentronsRepository,
    source_location: str,
    format_string: str,
    head: str,
    expected_value: str,
) -> None:
    """Confirm that get_build_args is working as expected."""
    assert (
        get_build_args(source_repo, source_location, format_string, head)
        == expected_value
    )


@pytest.mark.parametrize(
    "image_name,build_args,expected_value",
    [
        [
            "test-image:latest",
            None,
            BuildItem(
                context=DOCKERFILE_DIR_LOCATION, target="test-image:latest", args=None
            ),
        ],
        [
            "test-image:latest",
            ListOrDict(
                __root__={
                    "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons"
                    "/ot3-firmware/archive/refs"
                    "/heads/main.zip"
                }
            ),
            BuildItem(
                context=DOCKERFILE_DIR_LOCATION,
                target="test-image:latest",
                args=ListOrDict(
                    __root__={
                        "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/"
                        "Opentrons/ot3-firmware/"
                        "archive/refs/heads/"
                        "main.zip"
                    }
                ),
            ),
        ],
    ],
)
def test_get_service_build(
    image_name: str, build_args: Optional[ListOrDict], expected_value: BuildItem
) -> None:
    """Confirm that get_service_build works as expected."""
    assert get_service_build(image_name, build_args) == expected_value
