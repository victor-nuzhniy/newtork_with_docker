"""Module for bot utils."""
from typing import Dict

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_config_data_from_file(file_path: str) -> Dict:
    """Load config file data and create config data dict."""
    stream = open(file_path, mode="r")
    return load(stream, Loader)
