"""Schemas module for 'api' app."""
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
