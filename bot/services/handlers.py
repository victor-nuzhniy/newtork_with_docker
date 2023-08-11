"""Module for bot handlers."""
from typing import Dict, Optional

from .urls import urls
from .utils import make_request


def register_user(username: str, password: str) -> None:
    """Register user on 'network' api."""
    url: str = urls.get_signup_user_url()
    method: str = "post"
    headers: Dict = dict()
    data: Dict = {"username": username, "password": password}
    make_request(url, method, headers, data)


def get_user_tokens(user_data: Dict) -> Dict:
    """Get user tokens from 'network' api."""
    url: str = urls.get_tokens_url()
    method: str = "post"
    headers: Dict = dict()
    return make_request(url, method, headers, user_data)


def create_post(token: str, message: str) -> Optional[Dict]:
    """Create post by user."""
    url: str = urls.get_post_create_url()
    method: str = "post"
    headers: Dict = {"Authorization": f"Bearer {token}"}
    data: Dict = {"message": message}
    return make_request(url, method, headers, data)
