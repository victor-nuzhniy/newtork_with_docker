"""Factories for testing 'api' app models."""
import factory

from api.models import Like, Post, User
from tests.bases import BaseModelFactory


class UserFactory(BaseModelFactory):
    """Factory for testing custom User model."""

    class Meta:
        """Class Meta for UserFactory."""

        model = User
        exclude = ("post_set", "like_set")
        skip_postgeneration_save = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    is_staff = factory.Faker("pybool")
    is_active = factory.Faker("pybool")
    password = factory.django.Password("pw")
    post_set = factory.RelatedFactoryList(
        factory="tests.api.factories.PostFactory",
        factory_related_name="post_set",
        size=0,
    )
    like_set = factory.RelatedFactoryList(
        factory="tests.api.factories.LikeFactory",
        factory_related_name="like_set",
        size=0,
    )


class PostFactory(BaseModelFactory):
    """Factory for testing Post model."""

    class Meta:
        """Class Meta for PostFactory."""

        model = Post
        django_get_or_create = ("user",)
        exclude = ("like_set",)
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    message = factory.Faker("pystr", min_chars=1, max_chars=255)
    like_set = factory.RelatedFactoryList(
        factory="tests.api.factories.LikeFactory",
        factory_related_name="like_set",
        size=0,
    )


class LikeFactory(BaseModelFactory):
    """Factory for testing Like model."""

    class Meta:
        """Class Meta for LikeFactory."""

        model = Like
        django_get_or_create = ("user", "message")

    user = factory.SubFactory(UserFactory)
    message = factory.SubFactory(PostFactory)
    eval = factory.Faker("pybool")
