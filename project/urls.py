"""DjangoTemplateProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .monitoring import RequirementsViewSet

admin.site.site_header = f"{settings.PROJECT_NAME} {settings.PROJECT_SETTINGS} {settings.PROJECT_VERSION}"
admin.site.site_title = f"{settings.PROJECT_NAME} {settings.PROJECT_SETTINGS}"
admin.site.index_title = f"{settings.PROJECT_NAME}"


urlpatterns = [
    # admin
    path("_admin/", admin.site.urls),
    # requirements monitoring endpoint
    path("api/monitoring/requirements", RequirementsViewSet.as_view({"get": "list"}), name="requirements"),
    # drf-spectacular generated schema and ui
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# v0 api
urlpatterns += []

if "django_prometheus" in settings.INSTALLED_APPS:
    urlpatterns.append(path("", include("django_prometheus.urls")))

    from prometheus_client import Info

    info = Info("project_commit_hash", "Current commit hash of this instance")
    info.info({"commit_hash": settings.PROJECT_COMMIT_HASH})
    info = Info("project_version", "Current version")
    info.info({"version": settings.PROJECT_VERSION})
    info = Info("project_build_date", "Docker image build date")
    info.info({"build_date": settings.PROJECT_BUILD_DATE})
