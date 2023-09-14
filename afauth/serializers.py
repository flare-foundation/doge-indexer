from rest_framework import serializers
from rest_registration.api.serializers import PasswordConfirmSerializerMixin
from rest_registration.settings import registration_settings
from rest_registration.utils.validation import run_validators, validate_user_password, validate_user_password_confirm

from .models import AFUser


class AFUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFUser
        fields = ("first_name", "last_name", "email")


class RegisterAFUserSerializer(PasswordConfirmSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = AFUser
        fields = ("email", "first_name", "last_name", "password")

    def has_password_confirm_field(self):
        return registration_settings.REGISTER_SERIALIZER_PASSWORD_CONFIRM

    def validate(self, attrs):
        validators = [validate_user_password]
        if self.has_password_confirm_field():
            validators.append(validate_user_password_confirm)
        run_validators(validators, attrs)
        return attrs

    def create(self, validated_data):
        data = validated_data.copy()
        if self.has_password_confirm_field():
            del data["password_confirm"]
        return self.Meta.model.objects.create_user(**data)
