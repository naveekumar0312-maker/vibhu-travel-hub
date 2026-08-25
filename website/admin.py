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


from .models import FleetPartnerInquiry

@admin.register(FleetPartnerInquiry)
class FleetPartnerInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "mobile",
        "email",
        "city",
        "vehicle_type",
        "vehicle_count",
        "service_type",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "vehicle_type",
        "service_type",
        "city",
    )
    search_fields = (
        "name",
        "mobile",
        "email",
        "city",
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
    list_per_page = 25

    fieldsets = (
        ("Application Info", {
            "fields": (
                "name",
                "mobile",
                "email",
                "city",
            )
        }),
        ("Fleet Details", {
            "fields": (
                "vehicle_count",
                "vehicle_type",
                "service_type",
                "message",
            )
        }),
        ("Application Status", {
            "fields": (
                "status",
            )
        }),
        ("System Metadata", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


from .models import City, OneWayFare, OneWayBooking, RoundTripFare, RoundTripBooking

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)


@admin.register(OneWayFare)
class OneWayFareAdmin(admin.ModelAdmin):
    list_display = ("from_city", "to_city", "fare", "is_active", "updated_at")
    list_filter = ("is_active", "from_city", "to_city")
    search_fields = ("from_city", "to_city")
    list_editable = ("fare", "is_active")


@admin.register(OneWayBooking)
class OneWayBookingAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "email", "pickup_city", "drop_city", "pickup_date", "pickup_time", "status", "created_at")
    list_filter = ("status", "pickup_city", "drop_city", "created_at")
    search_fields = ("name", "mobile", "email", "pickup_city", "drop_city")
    list_editable = ("status",)
    readonly_fields = ("created_at",)


@admin.register(RoundTripFare)
class RoundTripFareAdmin(admin.ModelAdmin):
    list_display = ("from_city", "place", "distance_km", "trip_duration", "sedan_fare", "mini_fare", "is_active")
    list_filter = ("is_active", "from_city")
    search_fields = ("from_city", "place")
    list_editable = ("is_active",)


@admin.register(RoundTripBooking)
class RoundTripBookingAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "email", "pickup_city", "pickup_date", "pickup_time", "dropoff_date", "dropoff_time", "status", "created_at")
    list_filter = ("status", "pickup_city", "created_at")
    search_fields = ("name", "mobile", "email", "pickup_city")
    list_editable = ("status",)
    readonly_fields = ("created_at",)






