from __future__ import annotations

import os
from settings_models import ConfigurationSettings

# Mode Names
PRODUCTION_MODE_NAME = 'prod'
DEVELOPMENT_MODE_NAME = 'dev'

# Latest Git Commit
LATEST_KEYWORD = "latest"


# Root of repo
ROOT_DIR = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", ".."
    )
)

DEFAULT_CONFIGURATION_FILE_PATH = f"{ROOT_DIR}/configuration.json"
CONFIGURATION_FILE_LOCATION_VAR_NAME = 'CONFIGURATION_FILE_LOCATION'