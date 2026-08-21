from pathlib import Path
import os

# pyrefly: ignore [missing-import]
from decouple import config
# pyrefly: ignore [missing-import]
import dj_database_url

# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# SECURITY
# ==========================================

SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-change-this-key"
)

DEBUG = config(
    "DEBUG",
    default=True,
    cast=bool
)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost,.onrender.com,vibhutravelhub.com,www.vibhutravelhub.com"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "https://vibhutravelhub.com",
    "https://www.vibhutravelhub.com",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ==========================================
# INSTALLED APPS
# ==========================================

INSTALLED_APPS = [

    # Django Apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local App
    "website",
    "dashboard",
    "blog",
]

# ==========================================
# MIDDLEWARE
# ==========================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

# ==========================================
# ROOT URL
# ==========================================

ROOT_URLCONF = "travel.urls"

# ==========================================
# TEMPLATES
# ==========================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "website.context_processors.static_version",
                "website.context_processors.global_context",
            ],
        },
    },
]

# ==========================================
# WSGI
# ==========================================

WSGI_APPLICATION = "travel.wsgi.application"

# ==========================================
# DATABASE
# ==========================================


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travels',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
# ==========================================
# PASSWORD VALIDATION
# ==========================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ==========================================
# LANGUAGE
# ==========================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = False

# ==========================================
# STATIC FILES
# ==========================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0

# ==========================================
# MEDIA FILES
# ==========================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# ==========================================
# DEFAULT PRIMARY KEY
# ==========================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================================
# JAZZMIN SETTINGS
# ==========================================

JAZZMIN_SETTINGS = {

    "site_title": "Vibhu Travel Hub Admin",

    "site_header": "Vibhu Travel Hub",

    "site_brand": "Vibhu Travel Hub",

    "welcome_sign": "Welcome to Vibhu Travel Hub Administration",

    "copyright": "© 2026 Vibhu Travel Hub",

    "search_model": [
        "website.Vehicle",
        "website.Enquiry",
    ],

    "show_sidebar": True,

    "navigation_expanded": True,

    "sidebar_disable_expand": False,

    "related_modal_active": True,

    "changeform_format": "horizontal_tabs",

    "icons": {

        "website.vehicle": "fas fa-bus",

        "website.enquiry": "fas fa-phone-alt",

        "auth.user": "fas fa-user",

        "auth.group": "fas fa-users",

    },

    "default_icon_parents": "fas fa-folder",

    "default_icon_children": "fas fa-file",

    "theme": "darkly",

}

# ==========================================
# EMAIL CONFIGURATION
# ==========================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)
ADMIN_NOTIFICATION_EMAIL = config('ADMIN_NOTIFICATION_EMAIL', default=EMAIL_HOST_USER)