"""Module for bot urls."""
from .config import Config


class Urls:
    """Class for creating bot urls."""

    host: str = Config().get_var("host")

    def get_signup_user_url(self) -> str:
        """Get 'network' api signup user url."""
        return f"http://{self.host}/api/signup/"


urls = Urls()
