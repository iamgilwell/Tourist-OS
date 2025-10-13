import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from utils.enums import (BookingStatus, Currency, PaymentMethod, PaymentStatus,
                         Rating)


class Booking(models.Model):
    """
    Represents a tourist booking for a service
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tourist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "tourist"},
        related_name="bookings",
    )
    service = models.ForeignKey(
        "services.TourService", on_delete=models.CASCADE, related_name="bookings"
    )

    # Booking Details
    booking_date = models.DateTimeField(auto_now_add=True)
    service_date = models.DateField()
    service_time = models.TimeField()

    # Guest Information
    number_of_adults = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    number_of_children = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    guest_names = models.TextField(blank=True, help_text="Names of all guests")

    # Pricing
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.USD
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    final_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    # Status
    status = models.CharField(
        max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING
    )

    # Additional Information
    special_requests = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    # Confirmation
    confirmation_code = models.CharField(max_length=20, unique=True, blank=True)

    # Timestamps
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["-booking_date"]
        indexes = [
            models.Index(fields=["tourist", "status"]),
            models.Index(fields=["service_date"]),
            models.Index(fields=["status", "service_date"]),
            models.Index(fields=["confirmation_code"]),
        ]

    def __str__(self):
        return (
            f"{self.confirmation_code} - {self.tourist.username} - {self.service.name}"
        )

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = self.generate_confirmation_code()
        if not self.final_amount:
            self.final_amount = self.total_amount - self.discount_amount
        super().save(*args, **kwargs)

    def generate_confirmation_code(self):
        """Generate unique confirmation code"""
        import random
        import string

        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    @property
    def total_guests(self):
        """Total number of guests"""
        return self.number_of_adults + self.number_of_children

    @property
    def is_upcoming(self):
        """Check if booking is for a future date"""
        return self.service_date >= timezone.now().date()

    @property
    def is_past(self):
        """Check if booking is in the past"""
        return self.service_date < timezone.now().date()

    @property
    def can_cancel(self):
        """Check if booking can be cancelled (at least 24 hours before)"""
        if self.status not in [BookingStatus.CONFIRMED, BookingStatus.PENDING]:
            return False
        service_datetime = timezone.datetime.combine(
            self.service_date, self.service_time
        )
        if timezone.is_naive(service_datetime):
            service_datetime = timezone.make_aware(service_datetime)
        hours_until_service = (service_datetime - timezone.now()).total_seconds() / 3600
        return hours_until_service >= 24

    @property
    def can_review(self):
        """Check if booking can be reviewed (completed and past)"""
        return self.status == BookingStatus.COMPLETED and self.is_past


class Payment(models.Model):
    """
    Payment records for bookings - TRACKS YOUR REVENUE!
    """

    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="payment"
    )
    payment_id = models.CharField(
        max_length=100, blank=True, help_text="External payment gateway transaction ID"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.USD
    )
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    # Commission tracking (YOUR REVENUE!)
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("10.00"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Commission percentage (e.g., 10.00 for 10%)",
    )
    commission_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Your earnings from this booking",
    )
    provider_payout = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Amount to be paid to service provider",
    )

    # Payment Gateway Details
    gateway_response = models.JSONField(default=dict, blank=True)

    # Refund Information
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    refund_date = models.DateTimeField(null=True, blank=True)
    refund_reason = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["payment_id"]),
        ]

    def __str__(self):
        return f"Payment for {self.booking.confirmation_code} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        """Auto-calculate commission and provider payout"""
        if self.amount and self.commission_rate:
            self.commission_amount = (self.amount * self.commission_rate) / Decimal(
                "100"
            )
            self.provider_payout = self.amount - self.commission_amount
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        return self.status == PaymentStatus.COMPLETED

    @property
    def is_refunded(self):
        return self.status == PaymentStatus.REFUNDED


class Package(models.Model):
    """
    Pre-packaged multi-service offerings
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)
    destination = models.ForeignKey(
        "destinations.Destination", on_delete=models.CASCADE, related_name="packages"
    )
    services = models.ManyToManyField("services.TourService", through="PackageService")

    # Pricing
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Special discounted price",
    )
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.USD
    )

    # Details
    duration_days = models.PositiveIntegerField()
    max_capacity = models.PositiveIntegerField(default=10)
    included_items = models.TextField(blank=True)
    excluded_items = models.TextField(blank=True)

    # Media
    featured_image = models.ImageField(upload_to="packages/")
    gallery_images = models.JSONField(default=list, blank=True)

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
        verbose_name = "Package"
        verbose_name_plural = "Packages"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "is_featured"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        """Get the final price (discounted if available)"""
        return self.discounted_price if self.discounted_price else self.total_price

    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if (
            self.discounted_price
            and self.total_price
            and self.discounted_price < self.total_price
        ):
            return ((self.total_price - self.discounted_price) / self.total_price) * 100
        return 0


class PackageService(models.Model):
    """
    Through model for Package-Service relationship with sequencing
    """

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    service = models.ForeignKey("services.TourService", on_delete=models.CASCADE)
    day_number = models.PositiveIntegerField(
        help_text="Day number in the package itinerary"
    )
    sequence = models.PositiveIntegerField(help_text="Order within the day")
    start_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(
        blank=True, help_text="Special notes for this service in the package"
    )

    class Meta:
        ordering = ["day_number", "sequence"]
        unique_together = ["package", "service", "day_number"]
        verbose_name = "Package Service"
        verbose_name_plural = "Package Services"

    def __str__(self):
        return f"{self.package.name} - Day {self.day_number}: {self.service.name}"


class Review(models.Model):
    """
    Customer reviews for services
    """

    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="review"
    )
    tourist = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    service = models.ForeignKey(
        "services.TourService", on_delete=models.CASCADE, related_name="reviews"
    )

    # Rating & Review
    rating = models.PositiveIntegerField(choices=Rating.choices)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)

    # Additional Ratings
    value_for_money = models.PositiveIntegerField(
        choices=Rating.choices, null=True, blank=True
    )
    service_quality = models.PositiveIntegerField(
        choices=Rating.choices, null=True, blank=True
    )
    cleanliness = models.PositiveIntegerField(
        choices=Rating.choices, null=True, blank=True
    )

    # Moderation
    is_approved = models.BooleanField(default=False, help_text="Moderation status")
    admin_notes = models.TextField(blank=True)

    # Response from Provider
    provider_response = models.TextField(blank=True)
    provider_response_date = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ["booking", "tourist", "service"]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["service", "is_approved"]),
            models.Index(fields=["rating", "is_approved"]),
        ]

    def __str__(self):
        return f"{self.tourist.username} - {self.service.name} - {self.rating} stars"

    @property
    def average_rating(self):
        """Calculate average of all rating categories"""
        ratings = [self.rating]
        if self.value_for_money:
            ratings.append(self.value_for_money)
        if self.service_quality:
            ratings.append(self.service_quality)
        if self.cleanliness:
            ratings.append(self.cleanliness)
        return sum(ratings) / len(ratings) if ratings else 0
