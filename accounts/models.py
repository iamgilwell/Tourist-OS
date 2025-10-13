from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from utils.enums import UserType


class User(AbstractUser):
    """
    Custom user model extending AbstractUser for the tourist management system.
    Supports multiple user types: tourists, operators, DMOs, and admins.
    """

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.TOURIST,
        help_text="Type of user account",
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True, help_text="User biography or description")
    is_verified = models.BooleanField(
        default=False, help_text="Email/phone verification status"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["user_type", "is_active"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_tourist(self):
        return self.user_type == UserType.TOURIST

    @property
    def is_operator(self):
        return self.user_type == UserType.OPERATOR

    @property
    def is_dmo(self):
        return self.user_type == UserType.DMO

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class UserProfile(models.Model):
    """
    Extended profile information for users
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    preferences = models.JSONField(
        default=dict, blank=True, help_text="User preferences in JSON format"
    )
    language = models.CharField(max_length=10, default="en")
    timezone = models.CharField(max_length=50, default="UTC")
    newsletter_subscribed = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile of {self.user.username}"
