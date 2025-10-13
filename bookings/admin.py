from django.contrib import admin

from .models import Booking, Package, PackageService, Payment, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "confirmation_code",
        "tourist",
        "service",
        "service_date",
        "status",
        "final_amount",
        "created_at",
    ]
    list_filter = ["status", "service_date", "created_at"]
    search_fields = [
        "confirmation_code",
        "tourist__username",
        "tourist__email",
        "service__name",
    ]
    readonly_fields = [
        "id",
        "confirmation_code",
        "booking_date",
        "created_at",
        "updated_at",
        "total_guests",
    ]
    raw_id_fields = ["tourist", "service"]
    date_hierarchy = "service_date"

    fieldsets = (
        (
            "Booking Information",
            {
                "fields": (
                    "id",
                    "confirmation_code",
                    "tourist",
                    "service",
                    "booking_date",
                    "service_date",
                    "service_time",
                    "status",
                )
            },
        ),
        (
            "Guest Information",
            {
                "fields": (
                    "number_of_adults",
                    "number_of_children",
                    "total_guests",
                    "guest_names",
                )
            },
        ),
        (
            "Pricing",
            {"fields": ("total_amount", "discount_amount", "final_amount", "currency")},
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "special_requests",
                    "emergency_contact_name",
                    "emergency_contact_phone",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "confirmed_at",
                    "cancelled_at",
                    "completed_at",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "booking",
        "amount",
        "commission_amount",
        "provider_payout",
        "status",
        "method",
        "created_at",
    ]
    list_filter = ["status", "method", "created_at"]
    search_fields = ["booking__confirmation_code", "payment_id"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "commission_amount",
        "provider_payout",
    ]
    raw_id_fields = ["booking"]

    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "booking",
                    "payment_id",
                    "amount",
                    "currency",
                    "method",
                    "status",
                )
            },
        ),
        (
            "Commission Tracking (YOUR REVENUE!)",
            {
                "fields": ("commission_rate", "commission_amount", "provider_payout"),
                "classes": ("wide",),
            },
        ),
        (
            "Refund Information",
            {
                "fields": ("refund_amount", "refund_date", "refund_reason"),
                "classes": ("collapse",),
            },
        ),
        (
            "Gateway Details",
            {"fields": ("gateway_response",), "classes": ("collapse",)},
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "completed_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


class PackageServiceInline(admin.TabularInline):
    model = PackageService
    extra = 1
    raw_id_fields = ["service"]


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "destination",
        "duration_days",
        "final_price",
        "is_active",
        "is_featured",
    ]
    list_filter = ["is_active", "is_featured", "destination", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at", "final_price", "discount_percentage"]
    raw_id_fields = ["destination"]
    inlines = [PackageServiceInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "short_description",
                    "description",
                    "destination",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "total_price",
                    "discounted_price",
                    "final_price",
                    "discount_percentage",
                    "currency",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "duration_days",
                    "max_capacity",
                    "included_items",
                    "excluded_items",
                )
            },
        ),
        ("Media", {"fields": ("featured_image", "gallery_images")}),
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["tourist", "service", "rating", "is_approved", "created_at"]
    list_filter = ["rating", "is_approved", "created_at"]
    search_fields = ["tourist__username", "service__name", "comment"]
    readonly_fields = ["booking", "created_at", "updated_at", "average_rating"]
    raw_id_fields = ["tourist", "service", "booking"]

    fieldsets = (
        (
            "Review Information",
            {"fields": ("booking", "tourist", "service", "is_approved")},
        ),
        (
            "Rating",
            {
                "fields": (
                    "rating",
                    "value_for_money",
                    "service_quality",
                    "cleanliness",
                    "average_rating",
                )
            },
        ),
        ("Review Content", {"fields": ("title", "comment")}),
        (
            "Provider Response",
            {
                "fields": ("provider_response", "provider_response_date"),
                "classes": ("collapse",),
            },
        ),
        ("Moderation", {"fields": ("admin_notes",), "classes": ("collapse",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
