# pyrefly: ignore [missing-import]
from django.urls import path, include
# pyrefly: ignore [missing-import]
from django.conf import settings
# pyrefly: ignore [missing-import]
from django.conf.urls.static import static

# pyrefly: ignore [missing-import]
from django.contrib.sitemaps.views import sitemap
from website.sitemaps import StaticViewSitemap

# ==========================
# Sitemap Configuration
# ==========================

sitemaps = {
    "static": StaticViewSitemap,
}

# ==========================
# URL Patterns
# ==========================

urlpatterns = [

    # Custom Premium Admin
    path("admin/", include("dashboard.urls")),

    # Website
    path("", include("website.urls")),
    
    # Blog
    path("blog/", include("blog.urls")),

    # Dynamic Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),

]

# ==========================
# Media Files
# ==========================

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)