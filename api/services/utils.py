"""Module for 'api' app utilities."""
from datetime import datetime
from typing import Dict, Optional, Tuple

from django.utils.timezone import make_aware
from pytz import utc


def get_like(eval_data: str) -> Optional[bool]:
    """Get like value for using in Like serializer."""
    like: Optional[bool] = None
    if eval_data == "like":
        like = True
    elif eval_data == "dislike":
        like = False
    return like


def process_date_input(query_params: Dict) -> Optional[Tuple]:
    """
    Try to convert input data to datetime values.

    In case of ValueError return None.
    Return converted values.
    """
    try:
        date_from: datetime = datetime.strptime(
            query_params.get("date_from"), "%Y-%m-%d"
        )
        date_to: datetime = datetime.strptime(query_params.get("date_to"), "%Y-%m-%d")
        date_from = make_aware(date_from, utc)
        date_to = make_aware(date_to, utc)
    except ValueError:
        return None
    return date_from, date_to
