"""Class and function views for 'api' app."""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post, User
from .schemas import LikeSchema, user_register_schema
from .serializers import LikeSerializer, PostSerializer, UserSerializer
from .services.model_operations import get_like_instance


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

    def perform_create(self, serializer) -> None:
        """Add user to serializer and save Post instance."""
        serializer.save(user=self.request.user)


class LikeView(APIView):
    """Class with only POST method for creating Like with eval = True."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    schema = LikeSchema()

    def post(self, request, format=None) -> Response:
        """
        Create Like instance.

        If "eval" has value "Like", instance saves "eval" field with True.
        If "eval" has value "Dislike", instanse saves False.
        Otherwise - Response with "Invalid input data.".
        """
        message_id: int = request.data.get("message_id")
        user: User = request.user
        eval_data = request.data.get("eval").lower()
        if eval_data == "like":
            like: bool = True
        elif eval_data == "dislike":
            like = False
        else:
            return Response(
                {"result": "Invalid input data."}, status=status.HTTP_406_NOT_ACCEPTABLE
            )
        serializer = LikeSerializer(
            data={
                "user": user.pk,
                "message": message_id,
                "eval": like,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, format=None) -> Response:
        """Delete Like instance."""
        if like := get_like_instance(request.user, request.data.get("message_id")):
            like.delete()
            return Response({"result": "Like was successfully deleted."})
        return Response(
            {"result": "Like was not found"}, status=status.HTTP_404_NOT_FOUND
        )
