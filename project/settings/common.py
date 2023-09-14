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
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_registration",
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
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# djangorestframework-simplejwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=10),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
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

# django-rest-registration
REST_REGISTRATION = {
    "REGISTER_EMAIL_VERIFICATION_URL": f"{FRONTEND_URL}/account/verify-email",
    "REGISTER_OUTPUT_SERIALIZER_CLASS": "afauth.serializers.AFUserSerializer",
    "REGISTER_PASSWORD_VERIFICATION_ONE_TIME_USE": True,
    "REGISTER_SERIALIZER_CLASS": "afauth.serializers.RegisterAFUserSerializer",
    "REGISTER_VERIFICATION_ONE_TIME_USE": True,
    "REGISTER_VERIFICATION_PERIOD": timedelta(days=1),
    "REGISTER_VERIFICATION_URL": f"{FRONTEND_URL}/account/verify-user",
    "RESET_PASSWORD_VERIFICATION_URL": f"{FRONTEND_URL}/account/reset-password",
    "VERIFICATION_FROM_EMAIL": DEFAULT_FROM_EMAIL,
    "RESET_PASSWORD_VERIFICATION_PERIOD": timedelta(minutes=10),
    # Uncomment these when email templates are added
    # "REGISTER_VERIFICATION_EMAIL_TEMPLATES": {
    #     "html_body": "rest_registration/register/body.html",
    #     "text_body": "rest_registration/register/body.txt",
    #     "subject": "rest_registration/register/subject.txt",
    # },
    # "RESET_PASSWORD_VERIFICATION_EMAIL_TEMPLATES": {
    #     "html_body": "rest_registration/reset_password/body.html",
    #     "text_body": "rest_registration/reset_password/body.txt",
    #     "subject": "rest_registration/reset_password/subject.txt",
    # },
}

# django-types
from django.db.models.query import QuerySet

for cls in [QuerySet]:
    cls.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls)  # type: ignore [attr-defined]

# END OF DEPENDENCY SETTINGS
