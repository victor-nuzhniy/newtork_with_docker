"""Module for 'api' app admin site."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Like, Post, User


class CustomUserAdmin(UserAdmin):
    """Customized UserAdmin class with additional fields."""

    list_display = ("username", "email", "is_staff")
    search_fields = ("username", "email")
    readonly_fields = ("last_request_at",)
    fieldsets = (
        (None, {"fields": ("username", "last_name", "first_name", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "last_request_at")},
        ),
    )


class PostAdmin(admin.ModelAdmin):
    """Post model admin site settings."""

    list_display = ("id", "user", "message", "created_at")
    list_display_links = ("id", "user", "message")


class LikeAdmin(admin.ModelAdmin):
    """Like model admin site settings."""

    list_display = ("id", "user", "message", "eval")
    list_display_links = ("id", "user", "message")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
