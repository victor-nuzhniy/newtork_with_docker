"""Apps module for 'message' app."""
from django.apps import AppConfig


class MessagesConfig(AppConfig):
    """Config class for 'message' app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "messages"
