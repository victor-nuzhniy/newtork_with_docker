"""Class and function views for 'api' app."""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class RegisterView(APIView):
    """Class view for user registering."""

    def post(self, request: Request) -> Response:
        """Post data to create User."""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
