# pyrefly: ignore [missing-import]
from django.contrib import admin
# pyrefly: ignore [missing-import]
from django.utils.html import format_html
from .models import Enquiry, Vehicle, OutstationRoute


# ==========================================
# ENQUIRY ADMIN
# ==========================================

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "destination",
        "tourist_place",
        "travel_date",
        "status",
        "created_at",
    )

    list_filter = (
        "destination",
        "status",
        "travel_date",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "pickup",
        "drop",
        "destination",
        "tourist_place",
    )

    list_editable = (
        "status",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    list_per_page = 20

    fieldsets = (

        ("Customer Details", {

            "fields": (
                "name",
                "phone",
                "email",
            )

        }),

        ("Trip Information", {

            "fields": (
                "destination",
                "tourist_place",
                "pickup",
                "drop",
                "travel_date",
                "message",
            )

        }),

        ("Enquiry Status", {

            "fields": (
                "status",
            )

        }),

        ("System Information", {

            "classes": ("collapse",),

            "fields": (
                "created_at",
                "updated_at",
            )

        }),

    )


from .models import Enquiry, Vehicle, OutstationRoute, CitySEO


# ==========================================
# CITY SEO ADMIN
# ==========================================

@admin.register(CitySEO)
class CitySEOAdmin(admin.ModelAdmin):
    list_display = ("city_name", "slug", "meta_title", "updated_at")
    search_fields = ("city_name", "meta_title", "primary_keywords", "route_keywords")
    prepopulated_fields = {"slug": ("city_name",)}
    fieldsets = (
        ("City Information", {
            "fields": ("city_name", "slug")
        }),
        ("SEO Meta Data", {
            "fields": ("meta_title", "meta_description", "image_alt_text")
        }),
        ("Approved Keywords", {
            "fields": ("primary_keywords", "route_keywords")
        }),
        ("SEO Content Block", {
            "fields": ("seo_content",)
        }),
    )


@admin.register(OutstationRoute)
class OutstationRouteAdmin(admin.ModelAdmin):
    list_display = ("route_name", "destination_name", "starting_price", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("route_name", "destination_name")
    list_filter = ("is_active",)
    ordering = ("display_order",)
