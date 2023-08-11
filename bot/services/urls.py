"""Module for bot urls."""
from .config import Config


class Urls:
    """Class for creating bot urls."""

    host: str = Config().get_var("host")

    def get_signup_user_url(self) -> str:
        """Get 'network' api signup user url."""
        return f"http://{self.host}/api/signup/"

    def get_tokens_url(self) -> str:
        """Get 'network' api token obtain url."""
        return f"http://{self.host}/api/token/"

    def get_post_create_url(self) -> str:
        """Get 'network' api post creation url."""
        return f"http://{self.host}/api/post/"

    def get_like_create_url(self) -> str:
        """Get 'network' api like creation url."""
        return f"http://{self.host}/api/like/"


urls = Urls()
