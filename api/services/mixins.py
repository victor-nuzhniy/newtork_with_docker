"""Mixins module for 'api' app."""
from rest_framework.request import Request

from api.models import User


class UpdateRequestFieldMixin:
    """Class for adding functionality for updating user last_request_at field."""

    @staticmethod
    def perform_authentication(request: Request) -> None:
        """Add additional save operation for updating User last_request_at field."""
        user: User = request.user
        if user.is_authenticated:
            user.save()
