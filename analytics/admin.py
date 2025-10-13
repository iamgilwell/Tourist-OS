from django.contrib import admin

from .models import AnalyticsData, Promotion, Report


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "promotion_type",
        "price",
        "start_date",
        "end_date",
        "is_active",
        "is_paid",
        "conversions",
    ]
    list_filter = ["promotion_type", "is_active", "is_paid", "start_date", "end_date"]
    search_fields = ["title", "description"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "impressions",
        "clicks",
        "conversions",
        "click_through_rate",
        "conversion_rate",
        "is_currently_active",
    ]
    raw_id_fields = ["service", "package"]
    filter_horizontal = ["target_destinations", "target_categories"]

    fieldsets = (
        (
            "Promotion Information",
            {"fields": ("title", "description", "promotion_type", "image")},
        ),
        (
            "Target",
            {
                "fields": (
                    "service",
                    "package",
                    "target_destinations",
                    "target_categories",
                )
            },
        ),
        (
            "Pricing (REVENUE!)",
            {"fields": ("price", "currency", "is_paid"), "classes": ("wide",)},
        ),
        ("Duration", {"fields": ("start_date", "end_date", "is_currently_active")}),
        (
            "Performance Tracking",
            {
                "fields": (
                    "impressions",
                    "clicks",
                    "conversions",
                    "click_through_rate",
                    "conversion_rate",
                ),
                "classes": ("wide",),
            },
        ),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = [
        "metric_type",
        "value",
        "date_recorded",
        "destination",
        "service",
        "provider",
    ]
    list_filter = ["metric_type", "date_recorded"]
    search_fields = ["destination__name", "service__name", "provider__company_name"]
    readonly_fields = ["created_at"]
    raw_id_fields = ["destination", "service", "provider"]
    date_hierarchy = "date_recorded"

    fieldsets = (
        ("Metric Information", {"fields": ("metric_type", "value", "date_recorded")}),
        ("Scope", {"fields": ("destination", "service", "provider")}),
        ("Additional Data", {"fields": ("metadata",), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "report_type",
        "start_date",
        "end_date",
        "generated_by",
        "generated_at",
    ]
    list_filter = ["report_type", "generated_at", "start_date", "end_date"]
    search_fields = ["title", "destination__name", "provider__company_name"]
    readonly_fields = ["generated_at", "generated_by"]
    raw_id_fields = ["destination", "provider"]

    fieldsets = (
        ("Report Information", {"fields": ("title", "report_type")}),
        ("Scope", {"fields": ("destination", "provider")}),
        ("Period", {"fields": ("start_date", "end_date")}),
        ("Report Data", {"fields": ("data", "file"), "classes": ("wide",)}),
        (
            "Generation Info",
            {"fields": ("generated_by", "generated_at"), "classes": ("collapse",)},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)
