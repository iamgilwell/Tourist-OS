from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    """
    Represents a tourist destination (city, region, or specific location).
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(
        max_length=200, blank=True, help_text="Brief description for listings"
    )
    country = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    # Geolocation
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, help_text="Latitude coordinate"
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, help_text="Longitude coordinate"
    )

    # Media
    featured_image = models.ImageField(upload_to="destinations/")
    gallery_images = models.JSONField(
        default=list, blank=True, help_text="Array of image URLs"
    )

    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Management
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "dmo"},
        related_name="managed_destinations",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["country", "city"]),
            models.Index(fields=["is_active", "is_featured"]),
        ]

    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.city}")
        super().save(*args, **kwargs)

    @property
    def total_services(self):
        """Count total services in this destination"""
        from services.models import TourService

        return TourService.objects.filter(destination=self, is_active=True).count()


class Category(models.Model):
    """
    Categories for tourism services (Adventure, Cultural, Food, etc.)
    """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon class name for UI (e.g., 'fa-mountain')",
    )
    color = models.CharField(
        max_length=7, default="#000000", help_text="Hex color code for UI"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Amenity(models.Model):
    """
    Amenities available at destinations or services
    """

    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"
        ordering = ["name"]

    def __str__(self):
        return self.name
