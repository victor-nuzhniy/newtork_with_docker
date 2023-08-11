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

    def create_users_and_tasks(self) -> None:
        """Create given in config data number of users."""
        number_of_users = self.config.get_var("number_of_users")
        max_posts_per_user = self.config.get_var("max_posts_per_user")
        max_likes_per_user = self.config.get_var("max_likes_per_user")
        for index in range(number_of_users):
            username: str = fake.unique.first_name() + "_" + fake.last_name()
            password: str = fake.pystr(min_chars=50, max_chars=60)
            self.users_data.append({"username": username, "password": password})
            self.post_tasks[index] = fake.random_int(max=max_posts_per_user - 1)
            self.like_tasks[index] = fake.random_int(max=max_likes_per_user - 1)
            register_user(username, password)
