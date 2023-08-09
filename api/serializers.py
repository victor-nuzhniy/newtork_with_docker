"""Serializers for 'api' app."""

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer class."""

    class Meta:
        """Class Meta for User serializer class."""

        model = User
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        """Create user with validated_data."""
        user = User.objects.create(
            email=validated_data["email"], username=validated_data["name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
