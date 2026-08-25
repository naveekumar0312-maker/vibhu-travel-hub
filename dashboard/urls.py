# pyrefly: ignore [missing-import]
from django.urls import path, include
from .views.auth_views import dashboard_login, dashboard_logout, dashboard_home
from .views.enquiry_views import enquiry_list, enquiry_delete
from .views.fleet_views import fleet_list, fleet_create, fleet_edit, fleet_delete
from .views.subscriber_views import subscriber_list, subscriber_detail, subscriber_toggle, subscriber_delete
from .views.user_views import user_list
from .views.seo_views import seo_list, seo_edit

from .views.partner_enquiry_views import (
    partner_enquiry_list,
    partner_enquiry_detail,
    partner_enquiry_delete,
)

from .views.oneway_booking_views import (
    oneway_booking_list,
    oneway_booking_detail,
    oneway_booking_delete,
    oneway_fare_list,
)

from .views.management_roundtrip_views import (
    management_roundtrip_list,
    management_roundtrip_detail,
    management_roundtrip_status,
    management_roundtrip_delete,
)

from .views.hourly_fare_views import (
    hourly_fare_list,
    hourly_fare_create,
    hourly_fare_edit,
    hourly_fare_delete,
)

from .views.management_bulk_views import (
    management_bulk_list,
    management_bulk_detail,
    management_bulk_status,
    management_bulk_edit,
    management_bulk_delete,
)

urlpatterns = [
    # Auth
    path('', dashboard_login, name='dashboard_login'),
    path('login/', dashboard_login, name='management_login_alias'),
    path('logout/', dashboard_logout, name='dashboard_logout'),
    
    # Dashboard Home
    path('dashboard/', dashboard_home, name='dashboard_home'),
    
    # Bulk Bookings Management
    path('bulk-bookings/', management_bulk_list, name='management_bulk_list'),
    path('bulk-bookings/<int:pk>/', management_bulk_detail, name='management_bulk_detail'),
    path('bulk-bookings/<int:pk>/status/', management_bulk_status, name='management_bulk_status'),
    path('bulk-bookings/<int:pk>/edit/', management_bulk_edit, name='management_bulk_edit'),
    path('bulk-bookings/<int:pk>/delete/', management_bulk_delete, name='management_bulk_delete'),
    path('dashboard/bulk-bookings/', management_bulk_list, name='management_bulk_list_alias'),
    path('dashboard/bulk-bookings/<int:pk>/', management_bulk_detail, name='management_bulk_detail_alias'),
    
    # Round Trip Bookings Management
    path('round-trip/', management_roundtrip_list, name='management_roundtrip_list'),
    path('round-trip/<int:pk>/', management_roundtrip_detail, name='management_roundtrip_detail'),
    path('round-trip/<int:pk>/status/', management_roundtrip_status, name='management_roundtrip_status'),
    path('round-trip/<int:pk>/delete/', management_roundtrip_delete, name='management_roundtrip_delete'),
    path('dashboard/roundtrip-bookings/', management_roundtrip_list, name='management_roundtrip_list_alias'),
    path('dashboard/roundtrip-bookings/<int:pk>/', management_roundtrip_detail, name='management_roundtrip_detail_alias'),

    # Hourly Rental Pricing Management
    path('hourly-rental/', hourly_fare_list, name='management_hourly_fare_list'),
    path('hourly-rental/add/', hourly_fare_create, name='management_hourly_fare_create'),
    path('hourly-rental/<int:pk>/edit/', hourly_fare_edit, name='management_hourly_fare_edit'),
    path('hourly-rental/<int:pk>/delete/', hourly_fare_delete, name='management_hourly_fare_delete'),
    path('dashboard/hourly-fares/', hourly_fare_list, name='management_hourly_fare_list_alias'),

    # Customer Enquiries
    path('dashboard/enquiries/', enquiry_list, name='dashboard_enquiries'),
    path('dashboard/enquiries/<int:enquiry_id>/delete/', enquiry_delete, name='enquiry_delete'),

    # One Way Trip Bookings & Fares Management
    path('one-way/', oneway_booking_list, name='management_oneway_list'),
    path('oneway-trip/', oneway_booking_list, name='management_oneway_trip_alias'),
    path('dashboard/oneway-bookings/', oneway_booking_list, name='oneway_booking_list'),
    path('dashboard/oneway-bookings/<int:pk>/', oneway_booking_detail, name='oneway_booking_detail'),
    path('dashboard/oneway-bookings/<int:pk>/delete/', oneway_booking_delete, name='oneway_booking_delete'),
    path('dashboard/oneway-fares/', oneway_fare_list, name='oneway_fare_list'),

    # Partner Enquiries (Custom Management)
    path('dashboard/partner-enquiries/', partner_enquiry_list, name='partner_enquiries_list'),
    path('dashboard/partner-enquiries/<int:pk>/', partner_enquiry_detail, name='partner_enquiry_detail'),
    path('dashboard/partner-enquiries/<int:pk>/update/', partner_enquiry_detail, name='partner_enquiry_update'),
    path('dashboard/partner-enquiries/<int:pk>/delete/', partner_enquiry_delete, name='partner_enquiry_delete'),
    
    # Fleet
    path('dashboard/fleet/', fleet_list, name='dashboard_fleet'),
    path('dashboard/fleet/add/', fleet_create, name='fleet_create'),
    path('dashboard/fleet/<int:vehicle_id>/edit/', fleet_edit, name='fleet_edit'),
    path('dashboard/fleet/<int:vehicle_id>/delete/', fleet_delete, name='fleet_delete'),
    
    # City SEO
    path('dashboard/seo/', seo_list, name='dashboard_seo'),
    path('dashboard/seo/<int:city_id>/edit/', seo_edit, name='seo_edit'),
    
    # Subscribers
    path('dashboard/subscribers/', subscriber_list, name='dashboard_subscribers'),
    path('dashboard/subscribers/<int:sub_id>/', subscriber_detail, name='subscriber_detail'),
    path('dashboard/subscribers/<int:sub_id>/toggle/', subscriber_toggle, name='subscriber_toggle'),
    path('dashboard/subscribers/<int:sub_id>/delete/', subscriber_delete, name='subscriber_delete'),
    
    # Users
    path('dashboard/users/', user_list, name='dashboard_users'),
    
    # Blog
    path('dashboard/blog/', include('blog.dashboard_urls')),
]

