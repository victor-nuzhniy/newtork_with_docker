"""Module for bot functionality."""
from typing import Dict, List

from faker import Faker

from .config import Config
from .handlers import register_user

fake = Faker(["en_US"])


class Bot:
    """
    Class for creating bot.

    This bot is used for checking created 'network' api functionality.
    """

    def __init__(self) -> None:
        """Initialize bot instance creation."""
        self.config: Config = Config()
        self.post_tasks: Dict = dict()
        self.like_tasks: Dict = dict()
        self.users_data: List = []
        self.posts_number: int = 0
        self.user_tokens: List = []

    def create_users_and_tasks(self) -> None:
        """Create given in config data number of users."""
        number_of_users = self.config.get_var("number_of_users")
        max_posts_per_user = self.config.get_var("max_posts_per_user")
        max_likes_per_user = self.config.get_var("max_likes_per_user")
        for index in range(number_of_users):
            username: str = fake.unique.first_name() + "_" + fake.last_name()
            password: str = fake.pystr(min_chars=50, max_chars=60)
            posts_number: int = fake.random_int(min=1, max=max_posts_per_user)
            likes_number: int = fake.random_int(min=1, max=max_likes_per_user)
            self.users_data.append({"username": username, "password": password})
            self.post_tasks[index] = posts_number
            self.like_tasks[index] = likes_number
            self.posts_number += posts_number
            register_user(username, password)
