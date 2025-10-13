from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify

from utils.enums import (Currency, ServiceType, SubscriptionPlan,
                         SubscriptionStatus)


class ServiceProvider(models.Model):
    """
    Service providers (tour operators, hotels, activity providers, etc.)
    This is where you track your SaaS subscriptions!
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "operator"},
    )
    company_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    logo = models.ImageField(upload_to="provider_logos/", null=True, blank=True)
    banner_image = models.ImageField(
        upload_to="provider_banners/", null=True, blank=True
    )

    # Contact Information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    address = models.TextField()

    # Business Details
    business_registration_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)

    # Approval & Status
    is_approved = models.BooleanField(default=False, help_text="Admin approval status")
    is_verified = models.BooleanField(
        default=False, help_text="Business verification status"
    )

    # Location
    destination = models.ForeignKey(
        "destinations.Destination", on_delete=models.CASCADE, related_name="providers"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"
        ordering = ["company_name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_approved", "is_verified"]),
        ]

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        super().save(*args, **kwargs)

    @property
    def active_services_count(self):
        return self.services.filter(is_active=True).count()

    @property
    def average_rating(self):
        from bookings.models import Review

        avg = Review.objects.filter(service__provider=self, is_approved=True).aggregate(
            Avg("rating")
        )
        return avg["rating__avg"] or 0


class Subscription(models.Model):
    """
    SaaS subscription tracking for service providers (Revenue stream!)
    """

    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.CharField(
        max_length=20, choices=SubscriptionPlan.choices, default=SubscriptionPlan.FREE
    )
    status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.ACTIVE,
    )

    # Pricing
    monthly_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    # Plan Features
    max_services = models.PositiveIntegerField(
        default=5, help_text="Maximum number of services allowed"
    )
    max_bookings_per_month = models.PositiveIntegerField(default=100)
    analytics_enabled = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    featured_listing = models.BooleanField(default=False)

    # Subscription Period
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # Payment
    last_payment_date = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateTimeField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.provider.company_name} - {self.get_plan_display()}"


class TourService(models.Model):
    """
    Individual tourism services (tours, activities, transport, etc.)
    """

    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name="services"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)

    # Classification
    service_type = models.CharField(max_length=20, choices=ServiceType.choices)
    category = models.ForeignKey(
        "destinations.Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="services",
    )
    destination = models.ForeignKey(
        "destinations.Destination", on_delete=models.CASCADE, related_name="services"
    )

    # Pricing
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.USD
    )
    child_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    group_discount_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Discount percentage for groups (e.g., 10 for 10%)",
    )

    # Capacity & Duration
    max_capacity = models.PositiveIntegerField(
        default=1, help_text="Maximum number of guests per booking"
    )
    min_capacity = models.PositiveIntegerField(
        default=1, help_text="Minimum number of guests required"
    )
    duration_hours = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Duration in hours"
    )

    # Location Details
    meeting_point = models.CharField(max_length=255, blank=True)
    meeting_point_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    meeting_point_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    # Media
    featured_image = models.ImageField(upload_to="services/")
    gallery_images = models.JSONField(
        default=list, blank=True, help_text="Array of image URLs"
    )
    video_url = models.URLField(blank=True)

    # Details
    amenities = models.ManyToManyField(
        "destinations.Amenity", blank=True, related_name="services"
    )
    included_items = models.TextField(
        blank=True, help_text="What's included (one per line)"
    )
    excluded_items = models.TextField(
        blank=True, help_text="What's not included (one per line)"
    )
    requirements = models.TextField(
        blank=True, help_text="Requirements for participants"
    )
    cancellation_policy = models.TextField(blank=True)

    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tour Service"
        verbose_name_plural = "Tour Services"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["service_type", "destination"]),
            models.Index(fields=["is_active", "is_featured"]),
            models.Index(fields=["provider", "is_active"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.provider.company_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.provider.company_name}")
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        """Calculate average rating from approved reviews"""
        from bookings.models import Review

        avg = Review.objects.filter(service=self, is_approved=True).aggregate(
            Avg("rating")
        )
        return avg["rating__avg"]

    @property
    def total_reviews(self):
        """Count total approved reviews"""
        from bookings.models import Review

        return Review.objects.filter(service=self, is_approved=True).count()

    @property
    def total_bookings(self):
        """Count total bookings"""
        from bookings.models import Booking

        return Booking.objects.filter(service=self).count()


class AvailabilitySchedule(models.Model):
    """
    Defines availability schedules for services
    """

    service = models.ForeignKey(
        TourService, on_delete=models.CASCADE, related_name="availabilities"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Days of week (ISO standard: Monday=1, Sunday=7)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Availability Schedule"
        verbose_name_plural = "Availability Schedules"
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.service.name} - {self.start_date} to {self.end_date}"

    def is_available_on_day(self, day_name):
        """Check if service is available on a specific day"""
        day_mapping = {
            "monday": self.monday,
            "tuesday": self.tuesday,
            "wednesday": self.wednesday,
            "thursday": self.thursday,
            "friday": self.friday,
            "saturday": self.saturday,
            "sunday": self.sunday,
        }
        return day_mapping.get(day_name.lower(), False)


class Inventory(models.Model):
    """
    Daily inventory management for services
    """

    service = models.ForeignKey(
        TourService, on_delete=models.CASCADE, related_name="inventory"
    )
    date = models.DateField()
    available_slots = models.PositiveIntegerField()
    booked_slots = models.PositiveIntegerField(default=0)
    blocked_slots = models.PositiveIntegerField(
        default=0, help_text="Manually blocked slots"
    )
    price_override = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Override base price for this specific date",
    )
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
        unique_together = ["service", "date"]
        ordering = ["date"]
        indexes = [
            models.Index(fields=["service", "date"]),
            models.Index(fields=["date", "is_available"]),
        ]

    def __str__(self):
        return f"{self.service.name} - {self.date}"

    @property
    def remaining_slots(self):
        """Calculate remaining available slots"""
        return max(0, self.available_slots - self.booked_slots - self.blocked_slots)

    @property
    def current_price(self):
        """Get price for this date (override or base price)"""
        return self.price_override if self.price_override else self.service.base_price

    @property
    def is_fully_booked(self):
        """Check if service is fully booked"""
        return self.remaining_slots <= 0
