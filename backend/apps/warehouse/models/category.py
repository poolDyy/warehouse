from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.warehouse.choices import CategoryTypeChoices


class Category(BaseModel):
    user = models.ForeignKey(
        verbose_name=_('Пользователь'),
        to='users.User',
        on_delete=models.CASCADE,
        related_name='categories',
    )

    title = models.CharField(
        verbose_name=_('Категория'),
        max_length=255,
    )

    category_type = models.CharField(
        verbose_name=_('Тип категории'),
        max_length=255,
        choices=CategoryTypeChoices,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        indexes = [
            models.Index(fields=['user']),
        ]

    def user_obj_permission(self, user_id: int) -> bool:
        """Проверяет, имеет ли пользователь право на операцию над моделью."""
        return self.user_id == user_id
