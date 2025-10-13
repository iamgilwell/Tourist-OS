from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "username",
        "email",
        "user_type",
        "is_verified",
        "is_active",
        "date_joined",
    ]
    list_filter = ["user_type", "is_verified", "is_active", "is_staff", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name", "phone"]
    ordering = ["-date_joined"]

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": (
                    "user_type",
                    "phone",
                    "avatar",
                    "bio",
                    "is_verified",
                    "date_of_birth",
                    "country",
                    "city",
                    "address",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("user_type", "phone", "email")}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "language",
        "timezone",
        "newsletter_subscribed",
        "email_notifications",
    ]
    list_filter = ["newsletter_subscribed", "email_notifications", "sms_notifications"]
    search_fields = ["user__username", "user__email"]
    raw_id_fields = ["user"]
