import os
from datetime import datetime, timedelta

from django.utils.timezone import make_aware

# AFLABS PROJECT SETTINGS
PROJECT_NAME = "Doge Indexer"
PROJECT_SETTINGS = os.environ.get("DJANGO_SETTINGS_MODULE", "project.settings.local")
PROJECT_COMMIT_HASH = "local"
PROJECT_VERSION = "local"
PROJECT_BUILD_DATE = make_aware(datetime.now())  # noqa: DTZ005

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# DJANGO CORE SETTINGS

# A list of strings representing the host/domain names that this Django site can serve.
# This is a security measure to prevent HTTP Host header attacks, which are possible
# even under many seemingly-safe web server configurations.
ALLOWED_HOSTS = []

# database connection
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", ""),
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", ""),
    }
}

# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Start app in debug mode. This shows more detailed error messages. Should not be used
# in production
DEBUG = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email settings
SEND_EMAIL_CONFIRMATIONS = os.environ.get("SEND_EMAIL_CONFIRMATIONS") == "true"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")

et = os.environ.get("EMAIL_TIMEOUT", "")
try:
    EMAIL_TIMEOUT = int(et)
except ValueError:
    EMAIL_TIMEOUT = None

INSTALLED_APPS = [
    # builtin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # dependencies
    "rest_framework",
    "simple_history",
    "corsheaders",
    "drf_spectacular",
    # our apps
    "afauth.apps.AfauthConfig",
]

LANGUAGE_CODE = "en-us"

MEDIA_URL = "/media/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",  # Injects user in simple history
]

ROOT_URLCONF = "project.urls"

SECRET_KEY = os.environ.get("SECRET_KEY", "RUNNING_IN_LOCAL_MODE")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "django_templates")],
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


TIME_ZONE = "Europe/Ljubljana"

USE_I18N = True

USE_TZ = True

WSGI_APPLICATION = "project.wsgi.application"

# END OF DJANGO CORE

# AUTH

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "afauth.models.AFPasswordValidator",
    },
]

AUTH_USER_MODEL = "afauth.AFUser"

# END OF AUTH

# STATIC FILES

STATIC_URL = "/static/"

# END OF STATIC FILES

# AFLABS SPECIFIC APP SETTINGS
# if you add something here make sure you add it to .env.example if applicable

# deploy url for self referencing in emails, etc..
DEFAULT_WEB_URL = os.environ.get("DEFAULT_WEB_URL")

# requirements monitoring
REQUIREMENTS_FILE = os.environ.get("REQUIREMENTS_FILE", None)

# deploy url for self referencing in emails, etc..
FRONTEND_URL = os.environ.get("FRONTEND_URL")

# END OF AFLABS SPECIFIC APP SETTINGS

# DEPENDENCY SETTINGS

# djangorestframework
REST_FRAMEWORK = {
    # "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": f"{PROJECT_NAME} API",
    "DESCRIPTION": f"Api documentation for {PROJECT_NAME}",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/api/[0-9]",
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": False,
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}

# django-types
from django.db.models.query import QuerySet

for cls in [QuerySet]:
    cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore [attr-defined]

# END OF DEPENDENCY SETTINGS
