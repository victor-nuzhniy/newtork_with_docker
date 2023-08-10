"""Module for 'api' app model operations."""

from django.db.models import QuerySet

from api.models import Like, User


def get_like_instance(user: User, message_id: int) -> QuerySet:
    """Get Like instance by user and message_id."""
    return Like.objects.filter(user=user, message=message_id)
