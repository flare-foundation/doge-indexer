from .common import *

MEDIA_ROOT = "/appdata/media/"
STATIC_ROOT = "/tmp/staticroot/"

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [
    os.environ["ALLOWED_HOST"],
]

# django-cors-headers
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")

# Metrics export
if os.environ.get("EXPORT_METRICS", "") == "true":
    METRICS_EXTRA_TARGETS = ["database"]
    INSTALLED_APPS.append("django_prometheus")
    MIDDLEWARE = [
        "django_prometheus.middleware.PrometheusBeforeMiddleware",
        *MIDDLEWARE,
        "django_prometheus.middleware.PrometheusAfterMiddleware",
    ]
    DATABASES["default"]["engine"] = "django_prometheus.db.backends.postgresql"

try:
    with open(os.path.join(BASE_DIR, "PROJECT_COMMIT_HASH")) as f:
        PROJECT_COMMIT_HASH = f.read().strip()
except FileNotFoundError:
    pass

try:
    with open(os.path.join(BASE_DIR, "PROJECT_VERSION")) as f:
        PROJECT_VERSION = f.read().strip()
except FileNotFoundError:
    pass

try:
    with open(os.path.join(BASE_DIR, "PROJECT_BUILD_DATE")) as f:
        PROJECT_BUILD_DATE = f.read().strip()
except FileNotFoundError:
    pass

# sentry
if os.environ.get("SENTRY_DSN") is not None:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        integrations=[DjangoIntegration()],
        environment=os.environ["SENTRY_ENVIRONMENT"],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        release=f"{PROJECT_NAME}@{PROJECT_VERSION}",
    )
