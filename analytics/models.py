from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from utils.enums import MetricType, PromotionType


class Promotion(models.Model):
    """
    Promotional campaigns for services and packages (REVENUE GENERATOR!)
    Businesses pay YOU to promote their services
    """

    service = models.ForeignKey(
        "services.TourService",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="promotions",
    )
    package = models.ForeignKey(
        "bookings.Package",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="promotions",
    )
    promotion_type = models.CharField(max_length=20, choices=PromotionType.choices)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="promotions/", null=True, blank=True)

    # Target Audience
    target_destinations = models.ManyToManyField("destinations.Destination", blank=True)
    target_categories = models.ManyToManyField("destinations.Category", blank=True)

    # Pricing (what the business pays YOU for promotion)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="What the business pays for this promotion",
    )
    currency = models.CharField(max_length=3, default="USD")

    # Duration
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # Performance Tracking
    impressions = models.PositiveIntegerField(
        default=0, help_text="Number of times shown"
    )
    clicks = models.PositiveIntegerField(default=0, help_text="Number of clicks")
    conversions = models.PositiveIntegerField(
        default=0, help_text="Number of bookings generated"
    )

    # Status
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["is_active", "start_date", "end_date"]),
            models.Index(fields=["promotion_type", "is_active"]),
        ]

    def __str__(self):
        return f"{self.get_promotion_type_display()} - {self.title}"

    @property
    def is_currently_active(self):
        """Check if promotion is currently running"""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    @property
    def click_through_rate(self):
        """Calculate CTR (Click Through Rate)"""
        if self.impressions > 0:
            return (self.clicks / self.impressions) * 100
        return 0

    @property
    def conversion_rate(self):
        """Calculate conversion rate"""
        if self.clicks > 0:
            return (self.conversions / self.clicks) * 100
        return 0


class AnalyticsData(models.Model):
    """
    Analytics tracking for destinations and services (Can be sold as premium feature)
    """

    destination = models.ForeignKey(
        "destinations.Destination",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="analytics",
    )
    service = models.ForeignKey(
        "services.TourService",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="analytics",
    )
    provider = models.ForeignKey(
        "services.ServiceProvider",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="analytics",
    )

    # Metric Details
    metric_type = models.CharField(max_length=20, choices=MetricType.choices)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date_recorded = models.DateField()

    # Additional Context
    metadata = models.JSONField(
        default=dict, blank=True, help_text="Additional data in JSON format"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Analytics Data"
        verbose_name_plural = "Analytics Data"
        indexes = [
            models.Index(fields=["date_recorded", "metric_type"]),
            models.Index(fields=["destination", "metric_type"]),
            models.Index(fields=["service", "metric_type"]),
            models.Index(fields=["provider", "metric_type"]),
        ]
        ordering = ["-date_recorded"]

    def __str__(self):
        target = self.destination or self.service or self.provider
        return f"{target} - {self.get_metric_type_display()} - {self.date_recorded}"


class Report(models.Model):
    """
    Generated reports for DMOs and service providers
    """

    REPORT_TYPE_CHOICES = (
        ("daily", "Daily Report"),
        ("weekly", "Weekly Report"),
        ("monthly", "Monthly Report"),
        ("quarterly", "Quarterly Report"),
        ("annual", "Annual Report"),
        ("custom", "Custom Report"),
    )

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)

    # Scope
    destination = models.ForeignKey(
        "destinations.Destination",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports",
    )
    provider = models.ForeignKey(
        "services.ServiceProvider",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports",
    )

    # Report Period
    start_date = models.DateField()
    end_date = models.DateField()

    # Report Data
    data = models.JSONField(default=dict, help_text="Report data in JSON format")
    file = models.FileField(upload_to="reports/", null=True, blank=True)

    # Generation Info
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ["-generated_at"]

    def __str__(self):
        return f"{self.title} - {self.start_date} to {self.end_date}"
