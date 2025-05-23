from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class UserInfo(BaseModel):
    """Модель информации о пользователе."""

    user = models.OneToOneField(
        to='users.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='user_info',
    )

    first_name = models.CharField(
        verbose_name=_('Имя'),
        max_length=150,
    )

    second_name = models.CharField(
        verbose_name=_('Фамилия'),
        max_length=150,
    )

    middle_name = models.CharField(
        verbose_name=_('Отчество'),
        max_length=150,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Информация о пользователе')
        verbose_name_plural = _('Информация о пользователе')
        indexes = [
            models.Index(fields=['user']),
        ]
