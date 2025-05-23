from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.warehouse.choices import StorageTypeChoices


class Warehouse(BaseModel):
    """Склад продукции/материалов."""

    user = models.ForeignKey(
        verbose_name=_('Пользователь'),
        to='users.User',
        on_delete=models.CASCADE,
        related_name='warehouses',
    )

    categories = models.ManyToManyField(
        verbose_name=_('Категории'),
        to='warehouse.Category',
        related_name='warehouses',
    )

    title = models.CharField(
        verbose_name=_('Наименование'),
        max_length=255,
    )

    storage_type = models.CharField(
        verbose_name=_('Тип склада'),
        max_length=20,
        choices=StorageTypeChoices,
    )

    attachments = GenericRelation(
        'warehouse.FileAttachment',
        related_query_name='storage',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Склад')
        verbose_name_plural = _('Склад')
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self) -> str:
        return self.title

    def user_obj_permission(self, user_id: int) -> bool:
        """Проверяет, имеет ли пользователь право на операцию над моделью."""
        return self.user_id == user_id
