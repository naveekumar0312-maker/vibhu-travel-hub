from django.urls import path

from . import views

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

path("robots.txt", robots_txt, name="robots"),

# Fixed Destination Pages
path("destinations/tamil-nadu/", views.tamil_nadu_view, name="tamil_nadu_view"),
path("destinations/kerala/", views.kerala_view, name="kerala_view"),
path("destinations/karnataka/", views.karnataka_view, name="karnataka_view"),
path("subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
]