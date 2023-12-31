"""Configuration module for bot."""
from __future__ import annotations

import os.path
from typing import Any, Dict, Optional

from .utils import load_config_data_from_file


class Config:
    """Class for storing configurational data."""

    _data: Optional[Dict] = dict()
    _file_path: str = os.path.dirname(__file__) + "/../config.yaml"

    def __new__(cls, *args: Any, **kwargs: Any) -> Config:
        """Create new instance, if it's None, otherwise use earlier created one."""
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls.instance.__dict__ = load_config_data_from_file(cls._file_path)
        return cls.instance

    def get_var(self, name: str) -> Any:
        """Get config value by name."""
        return self.__dict__.get(name)


class LogConfig:
    """Class for storing logging configurational data."""

    _data: Optional[Dict] = dict()
    _file_path: str = os.path.dirname(__file__) + "/../logconfig.yaml"

    def __new__(cls, *args: Any, **kwargs: Any) -> LogConfig:
        """Create new instance, if it's None, otherwise user earlier created one."""
        if not hasattr(cls, "instance"):
            cls.instance = super(LogConfig, cls).__new__(cls, *args, **kwargs)
            cls.instance.__dict__ = load_config_data_from_file(cls._file_path)
        return cls.instance

    def get_config_dict(self) -> Dict:
        """Get logging config dict."""
        return self.__dict__
