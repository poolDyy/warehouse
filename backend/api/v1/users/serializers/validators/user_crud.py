from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

ERR = _('Используйте 8+ символов, включая заглавные, строчные буквы и цифры')


def validate_password(value: str) -> str | None:
    """Кастомный валидатор для пароля."""
    if len(value) < 8:
        raise ValidationError(ERR)

    has_digit = False
    has_upper = False
    has_lower = False

    for char in value:
        if char.isdigit():
            has_digit = True
        elif char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True

        if has_digit and has_upper and has_lower:
            return value

    if not has_digit:
        raise ValidationError(ERR)
    if not has_upper:
        raise ValidationError(ERR)
    if not has_lower:
        raise ValidationError(ERR)
