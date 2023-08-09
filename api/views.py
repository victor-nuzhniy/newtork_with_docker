"""Class and function views for 'api' app."""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post
from .schemas import user_register_schema
from .serializers import PostSerializer, UserSerializer


class RegisterView(APIView):
    """Class view for user registering."""

    schema = user_register_schema

    def post(self, request: Request) -> Response:
        """Post data to create User."""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostCreateView(generics.CreateAPIView):
    """Class with only POST method for creating message (post)."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        """Add user to serializer and save Post instance."""
        serializer.save(user=self.request.user)
