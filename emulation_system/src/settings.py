from __future__ import annotations

import os, json
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
SETTINGS = ConfigurationSettings.from_file_path(f"{ROOT_DIR}/configuration.json")
