from django.contrib import admin

from .models import (AvailabilitySchedule, Inventory, ServiceProvider,
                     Subscription, TourService)


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "destination",
        "is_approved",
        "is_verified",
        "created_at",
    ]
    list_filter = ["is_approved", "is_verified", "destination", "created_at"]
    search_fields = ["company_name", "description", "contact_email", "contact_phone"]
    prepopulated_fields = {"slug": ("company_name",)}
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["user", "destination"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("user", "company_name", "slug", "description", "destination")},
        ),
        ("Media", {"fields": ("logo", "banner_image")}),
        (
            "Contact Information",
            {"fields": ("contact_email", "contact_phone", "website", "address")},
        ),
        ("Business Details", {"fields": ("business_registration_number", "tax_id")}),
        ("Status", {"fields": ("is_approved", "is_verified")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "provider",
        "plan",
        "status",
        "monthly_price",
        "start_date",
        "end_date",
    ]
    list_filter = ["plan", "status", "start_date", "end_date"]
    search_fields = ["provider__company_name"]
    raw_id_fields = ["provider"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Subscription Info",
            {"fields": ("provider", "plan", "status", "monthly_price")},
        ),
        (
            "Plan Features",
            {
                "fields": (
                    "max_services",
                    "max_bookings_per_month",
                    "analytics_enabled",
                    "priority_support",
                    "featured_listing",
                )
            },
        ),
        (
            "Subscription Period",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "next_billing_date",
                    "last_payment_date",
                )
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(TourService)
class TourServiceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "provider",
        "service_type",
        "base_price",
        "currency",
        "is_active",
        "is_featured",
    ]
    list_filter = [
        "service_type",
        "is_active",
        "is_featured",
        "destination",
        "created_at",
    ]
    search_fields = ["name", "description", "provider__company_name"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["provider", "destination", "category"]
    filter_horizontal = ["amenities"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "provider",
                    "name",
                    "slug",
                    "short_description",
                    "description",
                )
            },
        ),
        ("Classification", {"fields": ("service_type", "category", "destination")}),
        (
            "Pricing",
            {
                "fields": (
                    "base_price",
                    "currency",
                    "child_price",
                    "group_discount_rate",
                )
            },
        ),
        (
            "Capacity & Duration",
            {"fields": ("max_capacity", "min_capacity", "duration_hours")},
        ),
        (
            "Location Details",
            {
                "fields": (
                    "meeting_point",
                    "meeting_point_latitude",
                    "meeting_point_longitude",
                )
            },
        ),
        ("Media", {"fields": ("featured_image", "gallery_images", "video_url")}),
        (
            "Details",
            {
                "fields": (
                    "amenities",
                    "included_items",
                    "excluded_items",
                    "requirements",
                    "cancellation_policy",
                )
            },
        ),
        (
            "SEO",
            {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)},
        ),
        ("Status", {"fields": ("is_active", "is_featured")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(AvailabilitySchedule)
class AvailabilityScheduleAdmin(admin.ModelAdmin):
    list_display = [
        "service",
        "start_date",
        "end_date",
        "start_time",
        "end_time",
        "is_active",
    ]
    list_filter = ["is_active", "start_date", "end_date"]
    search_fields = ["service__name"]
    raw_id_fields = ["service"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        "service",
        "date",
        "available_slots",
        "booked_slots",
        "remaining_slots",
        "is_available",
    ]
    list_filter = ["is_available", "date"]
    search_fields = ["service__name"]
    raw_id_fields = ["service"]
    readonly_fields = ["created_at", "updated_at", "remaining_slots"]
    date_hierarchy = "date"
