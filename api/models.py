"""Module for 'api' app models."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model."""

    last_request_at = models.DateTimeField(verbose_name="Last request at")
