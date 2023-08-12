"""Module for testing custom serializers method."""
from typing import Dict

import pytest
from faker import Faker

from api.models import User
from api.serializers import UserSerializer


@pytest.mark.django_db
class TestUserSerializerCreateMethod:
    """Class for testing UserSerializer create method."""

    pytestmark = pytest.mark.django_db

    def test_create(self, faker: Faker) -> None:
        """Test create method."""
        validate_data: Dict = {
            "username": faker.first_name(),
            "email": faker.email(),
            "password": faker.pystr(min_chars=50, max_chars=100),
        }
        serializer = UserSerializer()
        serializer.create(validate_data)
        user = User.objects.last()
        assert user.username == validate_data.get("username")
        assert user.email == validate_data.get("email")

    def test_create_without_email(self, faker: Faker) -> None:
        """Test create method. Email is empty."""
        validate_data: Dict = {
            "username": faker.first_name(),
            "password": faker.pystr(min_chars=50, max_chars=100),
        }
        serializer = UserSerializer()
        serializer.create(validate_data)
        user = User.objects.last()
        assert user.username == validate_data.get("username")
        assert user.email == validate_data.get("email", "")
