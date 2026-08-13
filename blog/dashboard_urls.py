# pyrefly: ignore [missing-import]
from django.urls import path
from . import dashboard_views

urlpatterns = [
    # Blog Posts
    path('', dashboard_views.dashboard_blog_list, name='dashboard_blog_list'),
    path('add/', dashboard_views.dashboard_blog_create, name='dashboard_blog_create'),
    path('<int:post_id>/edit/', dashboard_views.dashboard_blog_edit, name='dashboard_blog_edit'),
    path('<int:post_id>/delete/', dashboard_views.dashboard_blog_delete, name='dashboard_blog_delete'),
    path('<int:post_id>/toggle/', dashboard_views.dashboard_blog_toggle, name='dashboard_blog_toggle'),
]
