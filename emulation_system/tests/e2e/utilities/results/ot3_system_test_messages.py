"""Dataclass and constants representing test result descriptions."""

from tests.e2e.utilities.results.single_test_description import TestDescription

MONOREPO_BUILDER_CREATED = TestDescription(
    desc="Confirming monorepo builder was created",
)

MONOREPO_BUILDER_NOT_CREATED = TestDescription(
    desc="Confirming monorepo builder was not created",
)

OT3_FIRMWARE_BUILDER_CREATED = TestDescription(
    desc="Confirming ot3-firmware builder was created",
)

OT3_FIRMWARE_BUILDER_NOT_CREATED = TestDescription(
    desc="Confirming ot3-firmware builder was not created",
)

OPENTRONS_MODULES_BUILDER_CREATED = TestDescription(
    desc="Confirming opentrons-modules builder was created",
)

OPENTRONS_MODULES_BUILDER_NOT_CREATED = TestDescription(
    desc="Confirming opentrons-modules builder was not created",
)

MONOREPO_SOURCE_MOUNTED = TestDescription(
    desc="Confirming monorepo builder has local source mounted",
)

MONOREPO_SOURCE_NOT_MOUNTED = TestDescription(
    desc="Confirming monorepo builder does not have local source mounted",
)

OT3_FIRMWARE_SOURCE_MOUNTED = TestDescription(
    desc="Confirming ot3-firmware builder has local source mounted",
)

OT3_FIRMWARE_SOURCE_NOT_MOUNTED = TestDescription(
    desc="Confirming ot3-firmware builder does not have local source mounted",
)

OPENTRONS_MODULES_SOURCE_MOUNTED = TestDescription(
    desc="Confirming opentrons-modules builder has local source mounted",
)

OPENTRONS_MODULES_SOURCE_NOT_MOUNTED = TestDescription(
    desc="Confirming opentrons-modules builder does not have local source mounted",
)
