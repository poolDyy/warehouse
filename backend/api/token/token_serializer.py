from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict) -> dict:
        email = attrs.get(self.username_field)
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                {
                    'email': _('Необходимо указать почту'),
                    'password': _('Необходимо указать пароль'),
                }
            )

        User = get_user_model()

        try:
            user = User._default_manager.get_by_natural_key(email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    'email': _('Пользователь не найден'),
                }
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {
                    'email': _('Учетная запись неактивна'),
                }
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {
                    'password': _('Неверный пароль'),
                }
            )

        authenticate_kwargs = {
            self.username_field: email,
            'password': password,
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise serializers.ValidationError(
                {
                    'email': _('Учетная запись неактивна'),
                }
            )

        refresh = self.get_token(self.user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        if api_settings.UPDATE_LAST_LOGIN:
            from django.contrib.auth.models import update_last_login

            update_last_login(None, self.user)

        return data
