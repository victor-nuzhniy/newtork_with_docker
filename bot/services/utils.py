"""Module for bot utils."""
from typing import Dict, Optional

import requests
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_config_data_from_file(file_path: str) -> Dict:
    """Load config file data and create config data dict."""
    stream = open(file_path, mode="r")
    return load(stream, Loader)


def make_request(
    url: str, method: str, headers: Dict, data: Optional[Dict] = None
) -> Optional[Dict]:
    """Request url with method, headers and data."""
    headers.update({"Content-Type": "application/json"})
    handler = getattr(requests, method.lower())
    response = handler(url=url, headers=headers, json=data)
    if hasattr(response, "json"):
        return response.json()
