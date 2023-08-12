"""Module for testing 'api' app tables."""
import pytest

from api.models import Like, Post, User
from tests.api.factories import LikeFactory, PostFactory, UserFactory
from tests.bases import BaseModelFactory


@pytest.mark.django_db
class TestUser:
    """Class for testing User model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test User model instance creation."""
        BaseModelFactory.check_factory(factory_class=UserFactory, model=User)

    def test__str__(self) -> None:
        """Test User __str__ method."""
        obj: User = UserFactory()
        expected_result = str(obj.username)
        assert expected_result == obj.__str__()


@pytest.mark.django_db
class TestPost:
    """Class for testing User model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test User model instance creation."""
        BaseModelFactory.check_factory(factory_class=PostFactory, model=Post)

    def test__str__(self) -> None:
        """Test User __str__ method."""
        obj: Post = PostFactory()
        expected_result = f"Posted by {obj.user} {obj.created_at}"
        assert expected_result == obj.__str__()


@pytest.mark.django_db
class TestLike:
    """Class for testing User model."""

    pytestmark = pytest.mark.django_db

    def test_factory(self) -> None:
        """Test User model instance creation."""
        BaseModelFactory.check_factory(factory_class=LikeFactory, model=Like)

    def test__str__(self) -> None:
        """Test User __str__ method."""
        obj: Like = LikeFactory()
        expected_result = f"Like by {obj.user} {obj.created_at}"
        assert expected_result == obj.__str__()
