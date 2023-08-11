"""Module for bot functionality."""
import random
from typing import Dict, List

from faker import Faker

from .config import Config
from .handlers import create_like, create_post, get_user_tokens, register_user

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
        self.posts_ids: List = []
        self.user_tokens: List = []

    def create_users_and_tasks(self) -> None:
        """Create given in config data number of users."""
        number_of_users = self.config.get_var("number_of_users")
        for index in range(number_of_users):
            username: str = fake.unique.first_name() + "_" + fake.last_name()
            password: str = fake.pystr(min_chars=50, max_chars=60)
            self.add_task(index, "max_posts_per_user", self.post_tasks)
            self.add_task(index, "max_likes_per_user", self.like_tasks)
            self.users_data.append({"username": username, "password": password})
            register_user(username, password)

    def add_task(self, index: int, var_name: str, container: Dict) -> None:
        """Add task to its container."""
        max_number: int = self.config.get_var(var_name)
        number: int = fake.random_int(min=1, max=max_number)
        container[index] = number

    def get_users_tokens(self) -> None:
        """Fetch user access token from 'network' api."""
        for data in self.users_data:
            token_data: Dict = get_user_tokens(data)
            self.user_tokens.append(token_data)

    def perform_post_tasks(self) -> None:
        """Create posts in accordance with posts_task list."""
        while self.post_tasks:
            index: int = random.choice(list(self.post_tasks.keys()))
            token: str = self.user_tokens[index].get("access")
            message: str = fake.pystr(min_chars=1, max_chars=255)
            result = create_post(token, message)
            if result:
                self.posts_ids.append(result.get("id", 1))
            self.post_tasks[index] -= 1
            if self.post_tasks[index] == 0:
                self.post_tasks.pop(index)

    def perform_like_tasks(self) -> None:
        """Create likes in accordance with like_tasks list."""
        while self.like_tasks:
            index: int = random.choice(list(self.like_tasks.keys()))
            token: str = self.user_tokens[index].get("access")
            like: str = random.choice(["Like", "Dislike"])
            message_id: int = random.choice(self.posts_ids)
            create_like(token, message_id, like)
            self.like_tasks[index] -= 1
            if self.like_tasks[index] == 0:
                self.like_tasks.pop(index)
