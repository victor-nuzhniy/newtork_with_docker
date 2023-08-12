"""Module for testing 'api' app views."""
from typing import Dict

import pytest
from django.test import Client
from django.urls import reverse
from faker import Faker

from api.models import Post, User
from tests.api.factories import PostFactory


@pytest.mark.django_db
class TestRegisterView:
    """Class for testing RegisterView."""

    pytestmark = pytest.mark.django_db

    def test_register_view(self, faker: Faker, client: Client) -> None:
        """Test RegisterView."""
        username: str = faker.first_name()
        password: str = faker.pystr(min_chars=30, max_chars=60)
        url: str = reverse("sign_up")
        data: Dict = {"username": username, "password": password}
        response = client.post(url, data=data)
        result: Dict = response.json()
        assert response.status_code == 200
        assert isinstance(result.get("id"), int)
        assert result.get("username") == username
        assert result.get("email") == ""

    def test_register_view_with_email(self, faker: Faker, client: Client) -> None:
        """Test RegisterView. Email."""
        username: str = faker.first_name()
        email: str = faker.email()
        password: str = faker.pystr(min_chars=30, max_chars=60)
        url: str = reverse("sign_up")
        data: Dict = {"username": username, "email": email, "password": password}
        response = client.post(url, data=data)
        result: Dict = response.json()
        assert response.status_code == 200
        assert isinstance(result.get("id"), int)
        assert result.get("username") == username
        assert result.get("email") == email


@pytest.mark.django_db
class TestPostCreateView:
    """Class for testing PostCreateView."""

    pytestmark = pytest.mark.django_db

    def test_post_create_view(
        self, client: Client, faker: Faker, django_user_model: User
    ) -> None:
        """Test PostCreateView."""
        user: User = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        token_url: str = reverse("token")
        token_data: Dict = {"username": user.username, "password": "password"}
        response = client.post(token_url, data=token_data)
        access_token = response.json().get("access")
        url: str = reverse("create_post")
        headers: Dict = {"Authorization": f"Bearer {access_token}"}
        message: str = faker.pystr(min_chars=1, max_chars=255)
        response = client.post(url, headers=headers, data={"message": message})
        result = response.json()
        result_message = Post.objects.last()
        assert response.status_code == 201
        assert result.get("message") == message
        assert isinstance(result.get("id"), int)
        assert result_message.message == message

    def test_post_create_view_empty_message(
        self, client: Client, faker: Faker, django_user_model: User
    ) -> None:
        """Test PostCreateView. Empty message."""
        user: User = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        token_url: str = reverse("token")
        token_data: Dict = {"username": user.username, "password": "password"}
        response = client.post(token_url, data=token_data)
        access_token = response.json().get("access")
        url: str = reverse("create_post")
        headers: Dict = {"Authorization": f"Bearer {access_token}"}
        message: str = ""
        response = client.post(url, headers=headers, data={"message": message})
        assert response.status_code == 400


@pytest.mark.django_db
class TestLikeView:
    """Class for testing LikeView."""

    pytestmark = pytest.mark.django_db

    def test_like_view_post_method(
        self, client: Client, faker: Faker, django_user_model: User
    ) -> None:
        """Test LikeView post method."""
        user: User = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        token_url: str = reverse("token")
        token_data: Dict = {"username": user.username, "password": "password"}
        response = client.post(token_url, data=token_data)
        access_token = response.json().get("access")
        url: str = reverse("like")
        headers: Dict = {"Authorization": f"Bearer {access_token}"}
        post: Post = PostFactory()
        response = client.post(
            url, headers=headers, data={"message_id": post.id, "eval": "like"}
        )
        result: Dict = response.json()
        assert response.status_code == 200
        assert result.get("eval") is True
        assert result.get("user") == user.pk
        assert result.get("message") == post.pk

    def test_like_view_post_method_message_id_not_exist(
        self, client: Client, faker: Faker, django_user_model: User
    ) -> None:
        """Test LikeView post method."""
        user: User = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        token_url: str = reverse("token")
        token_data: Dict = {"username": user.username, "password": "password"}
        response = client.post(token_url, data=token_data)
        access_token = response.json().get("access")
        url: str = reverse("like")
        headers: Dict = {"Authorization": f"Bearer {access_token}"}
        response = client.post(
            url,
            headers=headers,
            data={"message_id": faker.random_int(min=1), "eval": "like"},
        )
        assert response.status_code == 400

    def test_like_view_post_method_invalid_input(
        self, client: Client, faker: Faker, django_user_model: User
    ) -> None:
        """Test LikeView post method."""
        user: User = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        token_url: str = reverse("token")
        token_data: Dict = {"username": user.username, "password": "password"}
        response = client.post(token_url, data=token_data)
        access_token = response.json().get("access")
        url: str = reverse("like")
        headers: Dict = {"Authorization": f"Bearer {access_token}"}
        post: Post = PostFactory()
        response = client.post(
            url, headers=headers, data={"message_id": post.id, "eval": "likee"}
        )
        result: Dict = response.json()
        assert response.status_code == 406
        assert result.get("result") == "Invalid input data."

    def test_like_view_post_method_unauthorized(
        self, client: Client, faker: Faker, django_user_model: User
    ) -> None:
        """Test LikeView post method."""
        user: User = django_user_model.objects.create_superuser(
            username="test", email="test@gmail.com", password="password"
        )
        token_url: str = reverse("token")
        token_data: Dict = {"username": user.username, "password": "password"}
        response = client.post(token_url, data=token_data)
        access_token = response.json().get("access")
        url: str = reverse("like")
        headers: Dict = {"Authorization": f"Bearer {access_token}1"}
        response = client.post(
            url, headers=headers, data={"message_id": 5, "eval": "like"}
        )
        assert response.status_code == 401
