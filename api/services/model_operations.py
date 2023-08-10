"""Module for 'api' app model operations."""
from typing import Dict, List, Optional, Tuple

from django.db.models import Count, F, QuerySet

from api.models import Like, Post, User


def get_like_instance(user: User, message_id: int) -> QuerySet:
    """Get Like instance by user and message_id."""
    return Like.objects.filter(user=user, message=message_id)


def get_analitic_like_queryset(input_data: Tuple) -> List[Dict]:
    """Get Like queryset for analitic view and return as a list."""
    date_from, date_to = input_data
    return list(
        Like.objects.filter(created_at__range=(date_from, date_to))
        .annotate(date=F("created_at__date"))
        .values("date")
        .order_by("date")
        .annotate(likes=Count("eval"))
    )


def get_user_instance_data(pk: int) -> Optional[User]:
    """Get User instance last_login and last_request_at by pk."""
    return User.objects.filter(id=pk).only("last_login", "last_request_at").first()


def get_post_queryset() -> QuerySet:
    """Get Post model queryset."""
    return Post.objects.all()
