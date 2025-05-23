from rest_framework import serializers


def validate_telegram_username(value: str) -> str:
    """Валидатор для проверки наличия символа @ в telegram_username."""
    if not value.startswith('@'):
        raise serializers.ValidationError('Никнейм в Telegram должен начинаться со символа @.')
    return value
