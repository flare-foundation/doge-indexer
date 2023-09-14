"""
This module is copy pasted from rest_registration.api.urls and with some slight changes

1. we assume that rest_framework_simplejwt is used so no login/logout views
2. we change some endpoints; no trailing slash and some minor renamings
3. we fix schema for drf-spectacular using its 'blueprints' api
"""

from typing import NoReturn

from django.urls import path
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify
from rest_registration.api.views import (
    change_password,
    profile,
    register,
    reset_password,
    send_reset_password_link,
    verify_registration,
)


# drf-spectacular view fixes
# https://drf-spectacular.readthedocs.io/en/latest/blueprints.html
class FixedVerifyRegistrationView(OpenApiViewExtension):
    target_class = "rest_registration.api.views.register.VerifyRegistrationView"

    def view_replacement(self):
        from rest_registration.api.views.register import VerifyRegistrationSerializer

        class Fixed(self.target_class):
            serializer_class = VerifyRegistrationSerializer

            @extend_schema(responses=None)
            def post(self, request, *args, **kwargs) -> NoReturn:
                raise NotImplementedError("this is just mock view for schema generation")

        return Fixed


class FixedRegistrationView(OpenApiViewExtension):
    target_class = "rest_registration.api.views.register.RegisterView"

    def view_replacement(self):
        from afauth.serializers import AFUserSerializer, RegisterAFUserSerializer

        class Fixed(self.target_class):
            @extend_schema(request=RegisterAFUserSerializer, responses=AFUserSerializer)
            def post(self, request, *args, **kwargs) -> NoReturn:
                raise NotImplementedError("this is just mock view for schema generation")

        return Fixed


urlpatterns = [
    # register
    path("register", register, name="register"),
    path("register/verify", verify_registration, name="verify-registration"),
    # reset password
    path("password_reset", send_reset_password_link, name="send-reset-password-link"),
    path("password_reset/confirm", reset_password, name="reset-password"),
    # user
    path("user", profile, name="profile"),
    path("change_password", change_password, name="change-password"),
    # drf simplejwt
    path("token/login", token_obtain_pair, name="token-login"),
    path("token/refresh", token_refresh, name="token-refresh"),
    path("token/verify", token_verify, name="token-verify"),
]
