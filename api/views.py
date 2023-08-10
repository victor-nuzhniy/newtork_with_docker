"""Class and function views for 'api' app."""
from typing import Dict

from django.db.models import QuerySet
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .schemas import LikeSchema, analitics_schema, user_register_schema
from .serializers import LikeSerializer, PostSerializer, UserSerializer
from .services.mixins import UpdateRequestFieldMixin
from .services.model_operations import (
    get_analitic_like_queryset,
    get_like_instance,
    get_post_queryset,
    get_user_instance_data,
)
from .services.utils import get_like, process_date_input


class RegisterView(APIView):
    """Class view for user registering."""

    schema = user_register_schema

    def post(self, request: Request) -> Response:
        """Post data to create User."""
        user_data = self.perform_create(request.data)
        return Response(user_data)

    @staticmethod
    def perform_create(data: Dict) -> Dict:
        """Process input data and save user instance."""
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


class PostCreateView(UpdateRequestFieldMixin, generics.CreateAPIView):
    """Class with only POST method for creating message (post)."""

    queryset = get_post_queryset()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer) -> None:
        """Add user to serializer and save Post instance."""
        serializer.save(user=self.request.user)


class LikeView(UpdateRequestFieldMixin, APIView):
    """Class with only POST method for creating Like with eval = True."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    schema = LikeSchema()

    def post(self, request) -> Response:
        """
        Create Like instance.

        If "eval" has value "Like", instance saves "eval" field with True.
        "Dislike" - False.
        Otherwise - Response with "Invalid input data.".
        """
        message_id: int = request.data.get("message_id")
        user: User = request.user
        eval_data = request.data.get("eval").lower()
        if like := get_like(eval_data):
            return Response(
                {"result": "Invalid input data."}, status=status.HTTP_406_NOT_ACCEPTABLE
            )
        like_data = self.perform_create(message_id, user, like)
        return Response(like_data)

    @staticmethod
    def perform_create(message_id: int, user: User, like: bool) -> Dict:
        """Process input data and save Like instance."""
        serializer = LikeSerializer(
            data={
                "user": user.pk,
                "message": message_id,
                "eval": like,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete(self, request) -> Response:
        """Delete Like instance."""
        if like := get_like_instance(request.user, request.data.get("message_id")):
            self.perform_delete(like)
            return Response({"result": "Like was successfully deleted."})
        return Response(
            {"result": "Like was not found"}, status=status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def perform_delete(like: QuerySet) -> None:
        """Delete fetched instances."""
        like.delete()


class AnaliticView(UpdateRequestFieldMixin, APIView):
    """Class for view with like analitic."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    schema = analitics_schema

    @staticmethod
    def get(request: Request) -> Response:
        """
        Handle input and return analitics data.

        Input format - '%Y-%m-%d'.
        Return list with dates and likes per date in given range.
        """
        if input_data := process_date_input(request.query_params) is None:
            return Response(
                {"result": "Invalid input format."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        return Response({"analitics": get_analitic_like_queryset(input_data)})


class UserActivityView(APIView):
    """Class for fetching user activity data."""

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    @staticmethod
    def get(request, pk) -> Response:
        """
        Get user last_login and last_request_at data.

        Path parameter 'pk' - user pk to look activity at.
        """
        user = get_user_instance_data(pk)
        if user:
            return Response(
                {
                    "activity": {
                        "last_login": user.last_login,
                        "last_request_at": user.last_request_at,
                    }
                }
            )
