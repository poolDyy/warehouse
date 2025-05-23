from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    'StatusChoices',
    'LanguageChoices',
]


class StatusChoices(models.TextChoices):
    """Статусы записей моделей наследников от BaseModel."""

    PUBLISHED = 'published', _('Опубликовано')
    ARCHIVED = 'archived', _('Архивировано')


class LanguageChoices(models.TextChoices):
    """Варианты языка."""

    RU = 'ru', 'Русский'
    EN = 'en', 'English'
