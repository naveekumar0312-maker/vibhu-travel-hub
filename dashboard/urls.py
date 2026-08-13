# pyrefly: ignore [missing-import]
from django.urls import path, include
from .views.auth_views import dashboard_login, dashboard_logout, dashboard_home
from .views.enquiry_views import enquiry_list, enquiry_delete
from .views.fleet_views import fleet_list, fleet_create, fleet_edit, fleet_delete
from .views.subscriber_views import subscriber_list, subscriber_detail, subscriber_toggle, subscriber_delete
from .views.user_views import user_list

urlpatterns = [
    # Auth
    path('', dashboard_login, name='dashboard_login'),
    path('logout/', dashboard_logout, name='dashboard_logout'),
    
    # Dashboard Home
    path('dashboard/', dashboard_home, name='dashboard_home'),
    
    # Enquiries
    path('dashboard/enquiries/', enquiry_list, name='dashboard_enquiries'),
    path('dashboard/enquiries/<int:enquiry_id>/delete/', enquiry_delete, name='enquiry_delete'),
    
    # Fleet
    path('dashboard/fleet/', fleet_list, name='dashboard_fleet'),
    path('dashboard/fleet/add/', fleet_create, name='fleet_create'),
    path('dashboard/fleet/<int:vehicle_id>/edit/', fleet_edit, name='fleet_edit'),
    path('dashboard/fleet/<int:vehicle_id>/delete/', fleet_delete, name='fleet_delete'),
    
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
