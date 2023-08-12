"""Module for testing 'api' app services utils."""
from datetime import datetime
from typing import Dict, Optional, Tuple

from django.utils.timezone import make_aware
from faker import Faker
from pytz import utc

from api.services.utils import get_like, process_date_input


class TestGetLike:
    """Class for testing utils get_like function."""

    def test_get_like_none(self, faker: Faker) -> None:
        """Test get_like function arbitrary input."""
        result: Optional[bool] = get_like(faker.pystr(min_chars=3, max_chars=10))
        assert result is None

    def test_get_like_true(self) -> None:
        """Test get_like function 'like' input."""
        result: Optional[bool] = get_like("like")
        assert result is True

    def test_get_like_false(self) -> None:
        """Test get_like function 'dislike' input."""
        result: Optional[bool] = get_like("dislike")
        assert result is False


class TestProcessDateInput:
    """Class for testing utils process_date_input."""

    def test_process_date_input(self, faker: Faker) -> None:
        """Test utils process_date_input."""
        query_params: Dict = {
            "date_from": faker.date(),
            "date_to": faker.date(),
        }
        expected_date_from: datetime = datetime.strptime(
            query_params.get("date_from"), "%Y-%m-%d"
        )
        expected_date_to: datetime = datetime.strptime(
            query_params.get("date_to"), "%Y-%m-%d"
        )
        expected_date_from = make_aware(expected_date_from, utc)
        expected_date_to = make_aware(expected_date_to, utc)
        result: Optional[Tuple[datetime, datetime]] = process_date_input(query_params)
        assert result[0] == expected_date_from
        assert result[1] == expected_date_to

    def test_process_date_input_none(self, faker: Faker) -> None:
        """Test utils process_date_input result None."""
        query_params: Dict = {
            "date_from": faker.pystr(min_chars=1, max_chars=10),
            "date_to": faker.date(),
        }
        result: Optional[Tuple[datetime, datetime]] = process_date_input(query_params)
        assert result is None
