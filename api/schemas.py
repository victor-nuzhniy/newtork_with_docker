"""Schemas module for 'api' app."""
from typing import List

import coreapi
from rest_framework.schemas import AutoSchema

user_register_schema = AutoSchema(
    manual_fields=[
        coreapi.Field(
            name="username",
            required=True,
            location="form",
            description="Username",
        ),
        coreapi.Field(
            name="email",
            required=True,
            location="form",
            description="User email",
        ),
        coreapi.Field(
            name="password", required=True, location="form", description="User password"
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
                description="Message id",
            ),
        ]
        if method.lower() == "post":
            custom_fields += [
                coreapi.Field(
                    name="eval",
                    required=True,
                    location="form",
                    description="Like value",
                ),
            ]
        return self._manual_fields + custom_fields
