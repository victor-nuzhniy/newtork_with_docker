"""Schemas module for 'api' app."""
from typing import List

import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

user_register_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            name="username",
            required=True,
            location="form",
            schema=coreschema.String(description="Username."),
        ),
        coreapi.Field(
            name="email",
            required=True,
            location="form",
            schema=coreschema.String(description="User email."),
            description="User email",
        ),
        coreapi.Field(
            name="password",
            required=True,
            location="form",
            schema=coreschema.String(description="User password."),
        ),
    ],
)


class LikeSchema(AutoSchema):
    """Class for Like operation schema."""

    manual_fields: List = []

    def get_manual_fields(self, path, method) -> List:
        """Get manual_fields for different for POST and DELETE methods."""
        custom_fields: List = [
            coreapi.Field(
                name="message_id",
                required=True,
                location="form",
                schema=coreschema.String(description="Message id."),
            ),
        ]
        if method.lower() == "post":
            custom_fields += [
                coreapi.Field(
                    name="eval",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        description="Like value. Can only be 'Like' or 'Dislike'."
                    ),
                ),
            ]
        return self._manual_fields + custom_fields


analitics_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            name="date_from",
            required=True,
            location="query",
            schema=coreschema.String(description="Date from. Format '%Y-%m-%d'"),
        ),
        coreapi.Field(
            name="date_to",
            required=True,
            location="query",
            schema=coreschema.String(description="Date to. Format '%Y-%m-%d'"),
        ),
    ]
)
