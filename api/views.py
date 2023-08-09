"""Class and function views for 'api' app."""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .schemas import user_register_schema
from .serializers import UserSerializer


class RegisterView(APIView):
    """Class view for user registering."""

    schema = user_register_schema

    def post(self, request: Request) -> Response:
        """Post data to create User."""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
