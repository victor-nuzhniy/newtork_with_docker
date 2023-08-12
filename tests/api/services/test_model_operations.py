"""Module fot testing services model_operations."""
from datetime import date, datetime, timedelta
from typing import List, Optional

import freezegun
import pytest
from django.db.models import QuerySet
from faker import Faker

from api.models import Like, Post, User
from api.services.model_operations import (
    get_analitic_like_queryset,
    get_like_instance,
    get_likes_number,
    get_likes_queryset,
    get_post_queryset,
    get_posts_number,
    get_user_instance_data,
    get_users_number,
)
from tests.api.factories import LikeFactory, PostFactory, UserFactory


@pytest.mark.django_db
class TestGetLikeInstance:
    """Class for testing model_operations get_like_instance function."""

    pytestmark = pytest.mark.django_db

    def test_get_like_instance(self) -> None:
        """Test get_like_instance functions."""
        user: User = UserFactory()
        post: Post = PostFactory(user=user)
        LikeFactory.create_batch(size=3, message=post, user=user)
        result: QuerySet = get_like_instance(user, post.pk)
        for like in result:
            assert like.user == user
            assert like.message == post


@pytest.mark.django_db
class TestGetAnaliticLikeQuerySet:
    """Class for testing model_operations get_analitic_like_queryset."""

    pytestmark = pytest.mark.django_db

    def test_get_analitic_like_queryset_one_day(self, faker: Faker) -> None:
        """Test get_analitic_like_queryset. Only one day."""
        number: int = faker.random_int(min=3, max=10)
        LikeFactory.create_batch(size=number)
        date_from: datetime = datetime.today() - timedelta(days=1)
        date_to: datetime = datetime.today() + timedelta(days=1)
        result: List = get_analitic_like_queryset((date_from, date_to))
        assert len(result) == 1
        assert result[0].get("date") == date.today()
        assert result[0].get("likes") == number

    def test_get_analitic_like_queryset_many_days(
        self, faker: Faker, freezer: freezegun
    ) -> None:
        """Test get_analitic_like_queryset. Many days."""
        number: int = faker.random_int(min=3, max=10)
        dates: List[Optional[datetime]] = []
        numbers: List[Optional[int]] = []
        for i in range(number):
            dates.append(datetime.today() - timedelta(days=number - i))
            numbers.append(faker.random_int(min=3, max=10))
            freezer.move_to(dates[-1].strftime("%Y-%m-%d"))
            user: User = UserFactory()
            post: Post = PostFactory()
            LikeFactory.create_batch(size=numbers[-1], user=user, message=post)
        result = get_analitic_like_queryset(
            (dates[0] - timedelta(days=1), dates[-1] + timedelta(days=1))
        )
        for i, item in enumerate(result):
            assert item.get("date") == dates[number - i - 1]
            assert item.get("likes") == numbers[number - i - 1]


@pytest.mark.django_db
class TestGetUserInstanceData:
    """Class for testing model_operations get_user_instance_data."""

    pytestmark = pytest.mark.django_db

    def test_get_user_instance_data(self) -> None:
        """Test get_user_instance_data."""
        user: User = UserFactory()
        result = get_user_instance_data(user.pk)
        assert result.pk == user.pk
        assert result.last_login == user.last_login
        assert result.last_request_at == user.last_request_at


@pytest.mark.django_db
class TestGetPostQueryset:
    """Class for testing model_operations get_post_queryset."""

    pytestmark = pytest.mark.django_db

    def test_get_post_queryset(self, faker: Faker) -> None:
        """Test get_post_queryset."""
        size: int = faker.random_int(min=3, max=5)
        posts: List[Post] = PostFactory.create_batch(size=size)
        result: QuerySet = get_post_queryset()
        for i, post in enumerate(posts):
            assert post == result[i]


@pytest.mark.django_db
class TestGetUserNumber:
    """Class for testing model_operations get_users_number."""

    pytestmark = pytest.mark.django_db

    def test_get_users_number(self, faker: Faker) -> None:
        """Test get_users_number."""
        size: int = faker.random_int(min=3, max=5)
        UserFactory.create_batch(size=size)
        result = get_users_number()
        assert result == size


@pytest.mark.django_db
class TestGetPostNumber:
    """Class for testing model_operations get_posts_number."""

    pytestmark = pytest.mark.django_db

    def test_get_posts_number(self, faker: Faker) -> None:
        """Test get_posts_number."""
        size: int = faker.random_int(min=3, max=5)
        PostFactory.create_batch(size=size)
        result = get_posts_number()
        assert result == size


@pytest.mark.django_db
class TestLikesNumber:
    """Class for testing model_operations get_likes_number."""

    pytestmark = pytest.mark.django_db

    def test_get_likes_number(self, faker: Faker) -> None:
        """Test get_likes_number."""
        size: int = faker.random_int(min=3, max=5)
        user: User = UserFactory()
        LikeFactory.create_batch(size=size, user=user)
        result = get_likes_number()
        assert result == size


@pytest.mark.django_db
class TestGetLikesQueryset:
    """Class for testing model_operations get_likes_queryset."""

    pytestmark = pytest.mark.django_db

    def test_get_likes_queryset(self, faker: Faker) -> None:
        """Test get_likes_queryset."""
        size: int = faker.random_int(min=3, max=5)
        user: User = UserFactory()
        likes: List[Like] = LikeFactory.create_batch(size=size, user=user)
        result: QuerySet = get_likes_queryset()
        for i, post in enumerate(likes):
            assert post == result[i]
