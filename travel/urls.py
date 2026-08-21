# pyrefly: ignore [missing-import]
from django.urls import path, include
# pyrefly: ignore [missing-import]
from django.conf import settings
# pyrefly: ignore [missing-import]
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# ==========================
# URL Patterns
# ==========================

urlpatterns = [

    # Favicon
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "images/logo/logo.webp", permanent=True)),

    # Custom Premium Admin
    path("admin/", include("dashboard.urls")),

    # Website
    path("", include("website.urls")),
    
    # Blog
    path("blog/", include("blog.urls")),

]

# ==========================
# Media Files
# ==========================

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)