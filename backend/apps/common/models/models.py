from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models.choices import StatusChoices
from apps.common.models.managers import ArchivedManager, PublishedManager

__all__ = [
    'TimeStampedModel',
    'BaseModel',
]


class TimeStampedModel(models.Model):
    """Абстрактный класс. Содержит `статус` и `время создания / модификации` объекта."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления'),
    )

    class Meta:
        abstract = True
        ordering = ['-created']


class BaseModel(TimeStampedModel):
    """Абстрактный базовый класс моделей."""

    StatusChoices = StatusChoices

    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=20,
        choices=StatusChoices,
        default=StatusChoices.PUBLISHED,
    )

    updated_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name=_('Пользователь внесший изменения'),
        null=True,
    )

    objects = models.Manager()
    published = PublishedManager()
    archived = ArchivedManager()

    class Meta:
        abstract = True
        ordering = ['-created_at']
