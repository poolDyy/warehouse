from django.utils.translation import gettext_lazy as _

from api.common.serializers import serializers
from api.v1.users.serializers.validators import validate_password
from apps.users.models import User


class UserListRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для одного или нескольких пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_active',
            'created_at',
            'updated_at',
        )
        read_only_fields = fields


class UserCreateRequestSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    password = serializers.CharField(
        max_length=128,
        required=True,
        validators=[validate_password],
    )

    repeat_password = serializers.CharField(
        max_length=128,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'repeat_password',
        )

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({'password': _('Пароли не совпадают.')})
        return attrs

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )


class UserCreateResponseSerializer(serializers.ModelSerializer):
    """Сериалализато ответа на создание пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
        )
