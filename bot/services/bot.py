"""Module for bot functionality."""
import logging.config
import random
from typing import Dict, List

from faker import Faker

from .config import Config, LogConfig
from .handlers import create_like, create_post, get_user_tokens, register_user

fake = Faker(["en_US"])
logconfig = LogConfig()
logging.config.dictConfig(logconfig.get_config_dict())
logger = logging.getLogger(__name__)


class Bot:
    """
    Class for creating bot.

    This bot is used for checking created 'network' api functionality.
    """

    def __init__(self) -> None:
        """Initialize bot instance creation."""
        logger.info("Bot is in initialization process...")
        self.config: Config = Config()
        self.post_tasks: Dict = dict()
        self.like_tasks: Dict = dict()
        self.users_data: List = []
        self.posts_ids: List = []
        self.user_tokens: List = []

    def create_users_and_tasks(self) -> None:
        """Create given in config data number of users."""
        logger.info("Creating user and tasks.")
        number_of_users = self.config.get_var("number_of_users")
        for index in range(number_of_users):
            username: str = fake.unique.first_name() + "_" + fake.last_name()
            password: str = fake.pystr(min_chars=50, max_chars=60)
            post_number: int = self.add_task(
                index, "max_posts_per_user", self.post_tasks
            )
            like_number: int = self.add_task(
                index, "max_likes_per_user", self.like_tasks
            )
            self.users_data.append({"username": username, "password": password})
            register_user(username, password)
            logger.info(
                f"Created user {username} with tasks to create {post_number}"
                f" posts and {like_number} likes."
            )

    def add_task(self, index: int, var_name: str, container: Dict) -> int:
        """Add task to its container."""
        max_number: int = self.config.get_var(var_name)
        number: int = fake.random_int(min=1, max=max_number)
        container[index] = number
        return number

    def get_users_tokens(self) -> None:
        """Fetch user access token from 'network' api."""
        for data in self.users_data:
            token_data: Dict = get_user_tokens(data)
            self.user_tokens.append(token_data)

    def perform_post_tasks(self) -> None:
        """Create posts in accordance with posts_task list."""
        posts_number: int = sum(value for value in self.post_tasks.values())
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
        logger.info(f"Bot has created {posts_number} posts.")

    def perform_like_tasks(self) -> None:
        """Create likes in accordance with like_tasks list."""
        likes_number: int = sum(value for value in self.like_tasks.values())
        while self.like_tasks:
            index: int = random.choice(list(self.like_tasks.keys()))
            token: str = self.user_tokens[index].get("access")
            like: str = random.choice(["Like", "Dislike"])
            message_id: int = random.choice(self.posts_ids)
            create_like(token, message_id, like)
            self.like_tasks[index] -= 1
            if self.like_tasks[index] == 0:
                self.like_tasks.pop(index)
        logger.info(f"Bot has created {likes_number} likes.")

    def run_bot(self) -> None:
        """Run bot functionality."""
        self.create_users_and_tasks()
        self.get_users_tokens()
        self.perform_post_tasks()
        self.perform_like_tasks()
        logger.info("All tasks are successfully performed!")
