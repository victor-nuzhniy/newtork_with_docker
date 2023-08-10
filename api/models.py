"""Module for 'api' app models."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model."""

    last_request_at = models.DateTimeField(
        auto_now=True, verbose_name="Last request at"
    )


class Post(models.Model):
    """Model for 'api' posts."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Post author")
    message = models.CharField(max_length=255, verbose_name="Post message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self) -> str:
        """Represent model instance."""
        return f"Posted by {self.user} {self.created_at}"


class Like(models.Model):
    """Model for post like."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Like author")
    message = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post")
    eval = models.BooleanField(default=False, verbose_name="Evaluation")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self) -> str:
        """Represent model instance."""
        return f"Like by {self.user} {self.created_at}"
