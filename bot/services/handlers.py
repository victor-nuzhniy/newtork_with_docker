"""Module for bot handlers."""
from typing import Dict

from .urls import urls
from .utils import make_request


def register_user(username: str, password: str) -> None:
    """Register user on 'network' api."""
    url: str = urls.get_signup_user_url()
    method: str = "post"
    headers: Dict = dict()
    data: Dict = {"username": username, "password": password}
    make_request(url, method, headers, data)