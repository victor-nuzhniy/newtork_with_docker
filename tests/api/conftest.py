"""Module for tests api fixtures."""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import freezegun
import pytest
from django.test import Client
from django.urls import reverse
from faker import Faker

from api.models import Post, User
from tests.api.factories import LikeFactory, PostFactory, UserFactory


@pytest.fixture
def get_like_data_for_analitic(faker: Faker, freezer: freezegun) -> Tuple[List, List]:
    """
    Instantiate fake like data and return them.

    Data will be used for testing AnaliticView.
    """
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
    return dates, numbers


@pytest.fixture
def get_authorized_user_data(
    faker: Faker, django_user_model: User, client: Client
) -> Tuple[User, Dict]:
    """Create and get authorized user data for testing."""
    user = django_user_model.objects.create_superuser(
        username="test", email="test@gmail.com", password="password"
    )
    token_url: str = reverse("token")
    token_data: Dict = {"username": user.username, "password": "password"}
    response = client.post(token_url, data=token_data)
    access_token = response.json().get("access")
    headers: Dict = {"Authorization": f"Bearer {access_token}"}
    return user, headers
