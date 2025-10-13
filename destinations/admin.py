from django.contrib import admin

from .models import Amenity, Category, Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "country", "is_active", "is_featured", "created_at"]
    list_filter = ["is_active", "is_featured", "country", "created_at"]
    search_fields = ["name", "city", "country", "description"]
    prepopulated_fields = {"slug": ("name", "city")}
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["created_by"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "short_description",
                    "description",
                    "created_by",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "country",
                    "state_province",
                    "city",
                    "postal_code",
                    "latitude",
                    "longitude",
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "color", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ["name", "icon"]
    search_fields = ["name", "description"]
