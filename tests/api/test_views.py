"""Module for testing 'api' app views."""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import pytest
from django.test import Client
from django.urls import reverse
from faker import Faker

from api.models import Like, Post, User
from tests.api.factories import LikeFactory, PostFactory, UserFactory


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
        self, client: Client, faker: Faker, get_authorized_user_data: Tuple[User, Dict]
    ) -> None:
        """Test PostCreateView."""
        user, headers = get_authorized_user_data
        url: str = reverse("create_post")
        message: str = faker.pystr(min_chars=1, max_chars=255)
        response = client.post(url, headers=headers, data={"message": message})
        result = response.json()
        result_message = Post.objects.last()
        assert response.status_code == 201
        assert result.get("message") == message
        assert isinstance(result.get("id"), int)
        assert result_message.message == message

    def test_post_create_view_empty_message(
        self, client: Client, faker: Faker, get_authorized_user_data: Tuple[User, Dict]
    ) -> None:
        """Test PostCreateView. Empty message."""
        user, headers = get_authorized_user_data
        url: str = reverse("create_post")
        message: str = ""
        response = client.post(url, headers=headers, data={"message": message})
        assert response.status_code == 400

    def test_post_create_view_empty_message_unauthorized(
        self, client: Client, faker: Faker, get_authorized_user_data: Tuple[User, Dict]
    ) -> None:
        """Test PostCreateView. Unauthorized."""
        user, headers = get_authorized_user_data
        headers["Authorization"] += "1"
        url: str = reverse("create_post")
        message: str = "erw"
        response = client.post(url, headers=headers, data={"message": message})
        assert response.status_code == 401


@pytest.mark.django_db
class TestLikeView:
    """Class for testing LikeView."""

    pytestmark = pytest.mark.django_db

    def test_like_view_post_method(
        self, client: Client, faker: Faker, get_authorized_user_data: Tuple[User, Dict]
    ) -> None:
        """Test LikeView post method."""
        user, headers = get_authorized_user_data
        url: str = reverse("like")
        post: Post = PostFactory()
        response = client.post(
            url, headers=headers, data={"message_id": post.pk, "eval": "like"}
        )
        result: Dict = response.json()
        assert response.status_code == 200
        assert result.get("eval") is True
        assert result.get("user") == user.pk
        assert result.get("message") == post.pk

    def test_like_view_post_method_message_id_not_exist(
        self, client: Client, faker: Faker, get_authorized_user_data: Tuple[User, Dict]
    ) -> None:
        """Test LikeView post method. Message id isn't exist."""
        user, headers = get_authorized_user_data
        url: str = reverse("like")
        response = client.post(
            url,
            headers=headers,
            data={"message_id": faker.random_int(min=1), "eval": "like"},
        )
        assert response.status_code == 400

    def test_like_view_post_method_invalid_input(
        self, client: Client, faker: Faker, get_authorized_user_data: Tuple[User, Dict]
    ) -> None:
        """Test LikeView post method. Input is invalid."""
        user, headers = get_authorized_user_data
        url: str = reverse("like")
        post: Post = PostFactory()
        response = client.post(
            url, headers=headers, data={"message_id": post.pk, "eval": "likee"}
        )
        result: Dict = response.json()
        assert response.status_code == 406
        assert result.get("result") == "Invalid input data."

    def test_like_view_post_method_unauthorized(
        self, client: Client, faker: Faker, get_authorized_user_data: Tuple[User, Dict]
    ) -> None:
        """Test LikeView post method. Unauthorized."""
        user, headers = get_authorized_user_data
        headers["Authorization"] += "1"
        url: str = reverse("like")
        response = client.post(
            url, headers=headers, data={"message_id": 5, "eval": "like"}
        )
        assert response.status_code == 401

    def test_like_view_delete_method(
        self,
        client: Client,
        faker: Faker,
        get_authorized_user_data: Tuple[User, Dict],
    ) -> None:
        """Test LikeView delete method."""
        user, headers = get_authorized_user_data
        url: str = reverse("like")
        headers.update({"content-type": "application/json"})
        post: Post = PostFactory()
        LikeFactory.create_batch(size=4, message=post, user=user)
        response = client.delete(
            url, headers=headers, data=json.dumps({"message_id": post.pk})
        )
        result = response.json()
        assert response.status_code == 200
        assert result.get("result") == "Like was successfully deleted."
        assert not Like.objects.all()

    def test_like_view_delete_method_like_not_exist(
        self,
        client: Client,
        faker: Faker,
        get_authorized_user_data: Tuple[User, Dict],
    ) -> None:
        """Test LikeView delete method. Like is not exist."""
        user, headers = get_authorized_user_data
        url: str = reverse("like")
        headers.update({"content-type": "application/json"})
        post: Post = PostFactory()
        user: User = UserFactory()
        LikeFactory.create_batch(size=4, message=post, user=user)
        response = client.delete(
            url, headers=headers, data=json.dumps({"message_id": post.pk})
        )
        result = response.json()
        assert response.status_code == 404
        assert result.get("result") == "Like was not found"


@pytest.mark.django_db
class TestAnaliticView:
    """Class for testing AnaliticView."""

    pytestmark = pytest.mark.django_db

    def test_analitic_view(
        self,
        client: Client,
        faker: Faker,
        get_like_data_for_analitic: Tuple[List, List],
        get_authorized_user_data: Tuple[User, Dict],
    ) -> None:
        """Test AnaliticView."""
        dates, numbers = get_like_data_for_analitic
        number = len(dates)

        user, headers = get_authorized_user_data

        date_from: str = datetime.strftime(dates[0] - timedelta(days=1), "%Y-%m-%d")
        date_to: str = datetime.strftime(dates[-1] + timedelta(days=1), "%Y-%m-%d")
        url = reverse("analitics")
        response = client.get(
            url, headers=headers, data={"date_from": date_from, "date_to": date_to}
        )
        result = response.json().get("analitics")
        assert response.status_code == 200
        for i, item in enumerate(result):
            assert item.get("date") == dates[number - i - 1]
            assert item.get("likes") == numbers[number - i - 1]
