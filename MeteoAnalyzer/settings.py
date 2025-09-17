import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-=8pnlbsd@j!*0asdzdpqg44^d638yaj=fz6=d3mg8p^uuiy(dh"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") in ["TRUE", "True", "true", "t", "1"]

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "backend"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "core.apps.CoreConfig",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MeteoAnalyzer.urls"

REST_FRAMEWORK = {}

PAGE_SIZE = os.getenv("PAGE_SIZE", 10)

if PAGE_SIZE:
    PAGE_SIZE = int(PAGE_SIZE)
    REST_FRAMEWORK = {
        **REST_FRAMEWORK,
        **{
            "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
            "PAGE_SIZE": 10,
        },
    }

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {},
    "USE_SESSION_AUTH": False,
    "DEFAULT_AUTO_TAGS": False,
}


WSGI_APPLICATION = "MeteoAnalyzer.wsgi.application"


DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv(
            "DATABASE_URL",
            default="postgresql://database:database@database:5432/database",
        ),
    )
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

OPEN_METEO_CITY_ENDPOINT = os.getenv(
    "OPEN_METEO_CITY_ENDPOINT", "https://geocoding-api.open-meteo.com/v1/search"
)
OPEN_METEO_WEATHER_ENDPOINT = os.getenv(
    "OPEN_METEO_WEATHER_ENDPOINT", "https://archive-api.open-meteo.com/v1/archive"
)
