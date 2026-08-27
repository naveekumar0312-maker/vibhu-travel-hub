# pyrefly: ignore [missing-import]
from django.urls import path

from . import views
from dashboard.views import partner_enquiry_views as dashboard_partner_views
from website.views import robots_txt

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),
    
    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "send-enquiry/",
        views.send_enquiry,
        name="send_enquiry"
    ),

    path(
        "api/enquiry/submit/",
        views.api_submit_enquiry,
        name="api_submit_enquiry"
    ),


    path(
    "services/local-taxi-service/",
    views.local_taxi_service,
    name="local_taxi_service"
),

path(
    "services/bus-booking/",
    views.bus_booking,
    name="bus_booking"
),

path(
    "services/tempo-traveller/",
    views.tempo_traveller,
    name="tempo_traveller"
),

path(
    "services/outstation-tours/",
    views.outstation_tours,
    name="outstation_tours"
),

path(
    "services/pilgrimage-trips/",
    views.pilgrimage_trips,
    name="pilgrimage_trips"
),

path(
    "services/corporate-travel/",
    views.corporate_travel,
    name="corporate_travel"
),
path(
    "services/airport-transfer/",
    views.airport_transfer_service,
    name="airport_transfer"
),

# Service Aliases
path("services/taxi/", views.local_taxi_service, name="service_taxi_alias"),
path("services/local-taxi/", views.local_taxi_service, name="service_local_taxi_alias"),
path("services/outstation/", views.outstation_tours, name="service_outstation_alias"),
path("services/luxury-bus/", views.bus_booking, name="service_luxury_bus_alias"),
path("services/airport-transfers/", views.airport_transfer_service, name="service_airport_transfers_alias"),

path("robots.txt", views.robots_txt, name="robots"),
path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),

# State Destination Pages
path("destinations/tamil-nadu/", views.tamil_nadu_view, name="tamil_nadu_view"),
path("destinations/kerala/", views.kerala_view, name="kerala_view"),
path("destinations/karnataka/", views.karnataka_view, name="karnataka_view"),

# City Landing Pages
path("destinations/<slug:state_slug>/<slug:city_slug>/", views.city_detail_view, name="city_detail"),

# Tourist Place Landing Pages
path("destinations/<slug:state_slug>/<slug:city_slug>/<slug:place_slug>/", views.tourist_place_detail_view, name="tourist_place_detail"),
path("destinations/<slug:state_slug>/<slug:city_slug>/place/<slug:place_slug>/", views.tourist_place_detail_view, name="tourist_place_detail_place"),

# Book a Cab Pages (with Dropdown)
path("book-cab/", views.book_cab, name="book_cab"),
path("book-cab/one-way/", views.book_cab_one_way, name="book_cab_one_way"),
path("book-cab/round-trip/", views.book_cab_round_trip, name="book_cab_round_trip"),
path("book-cab/hourly/", views.book_cab_hourly, name="book_cab_hourly"),
path("book-cab/hourly-rental/", views.book_cab_hourly, name="book_cab_hourly_rental"),
path("book-cab/bulk/", views.book_cab_bulk, name="book_cab_bulk"),
path("book-cab/bulk-booking/", views.book_cab_bulk, name="book_cab_bulk_booking"),

# Backward Compatibility Route Aliases
path("book-trip/one-way/", views.book_cab_one_way, name="one_way_trip"),
path("book-trip/round-trip/", views.book_cab_round_trip, name="round_trip"),
path("book-trip/hourly-rental/", views.book_cab_hourly, name="hourly_rental"),
path("book-trip/bulk-booking/", views.book_cab_bulk, name="bulk_booking"),

# Fleet & Partner Pages
path("become-a-partner/", views.fleet_partner_view, name="partner"),
path("fleet-partner/", views.fleet_partner_view, name="fleet_partner"),
path("partner/", views.fleet_partner_view, name="partner_alias"),
path("fleet/", views.fleet_partner_view, name="fleet"),
path("api/partner/submit/", views.api_submit_fleet_partner, name="api_submit_fleet_partner"),

# Custom Internal Enquiry Management Aliases
path("enquiries/", dashboard_partner_views.partner_enquiry_list, name="custom_enquiries_list_alias"),
path("enquiries/<int:pk>/", dashboard_partner_views.partner_enquiry_detail, name="custom_enquiry_detail_alias"),
path("enquiries/<int:pk>/update/", dashboard_partner_views.partner_enquiry_detail, name="custom_enquiry_update_alias"),
]