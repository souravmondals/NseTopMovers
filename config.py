# ---------------------------------------------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------

"""Configuration management for the upskilling agent application."""

import os
from typing import Any, Dict

from dotenv import load_dotenv

load_dotenv()

# Default values as constants


class Config:
    """Application configuration class."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables with defaults."""
        result: Dict[str, Any] = {
            "USERNAME": os.getenv("USERNAME", ""),
            "PASSWORD": os.getenv("PASSWORD", ""),
            "PANCARD": os.getenv("PANCARD", ""),            
            "Excel-file-path": os.getenv("EXCEL_FILE_PATH", ""),
            "Fyers-ClientID": os.getenv("FYERS_CLIENT_ID", ""),
            "Fyers-Secret-Key": os.getenv("FYERS_SECRET_KEY", ""),
            "Fyers-Auth-Code": os.getenv("FYERS_AUTH_CODE", ""),           
        }
        return result

    def _parse_bool_env(self, env_var: str, default: bool = False) -> bool:
        """Parse boolean environment variable."""
        return os.getenv(env_var, str(default)).lower() == "true"

    def __getitem__(self, key: str) -> Any:
        """Get configuration value by key."""
        return self._config.get(key)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with optional default."""
        return self._config.get(key, default)

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()


config = Config()
