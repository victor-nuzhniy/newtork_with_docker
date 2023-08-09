"""Serializers for 'api' app."""

from rest_framework import serializers

from .models import Like, Post, User


class UserSerializer(serializers.ModelSerializer):
    """User model serializer class."""

    class Meta:
        """Class Meta for User serializer class."""

        model = User
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        """Create user with validated_data."""
        user = User.objects.create(
            email=validated_data["email"], username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    """Post model serializer class."""

    class Meta:
        """Class Meta for Post serializer class."""

        model = Post
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")


class LikeSerializer(serializers.ModelSerializer):
    """Like model serializer class."""

    class Meta:
        """Class Meta for Like serializer class."""

        model = Like
        fields = "__all__"
        read_only_fields = ("user", "created_at")
