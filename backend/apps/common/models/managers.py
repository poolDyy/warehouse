from django.db import models
from django.db.models import QuerySet

from apps.common.models.choices import StatusChoices

__all__ = [
    'PublishedManager',
    'ArchivedManager',
]


class PublishedManager(models.Manager):
    """Менеджер для работы с опубликованными записями."""

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=StatusChoices.PUBLISHED)


class ArchivedManager(models.Manager):
    """Менеджер для работы c записями в архиве."""

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=StatusChoices.ARCHIVED)
