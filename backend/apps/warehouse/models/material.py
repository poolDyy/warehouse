from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from .abs_storage_entity import StorageEntity


class Material(StorageEntity):
    """Материалы."""

    attachments = GenericRelation(
        'warehouse.FileAttachment',
        related_query_name='materials',
    )

    warehouse = models.ForeignKey(
        verbose_name=_('Склад'),
        to='warehouse.Warehouse',
        on_delete=models.CASCADE,
        related_name='materials',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Материал')
        verbose_name_plural = _('Материалы')
        indexes = [
            models.Index(fields=['warehouse']),
            models.Index(fields=['unit']),
        ]

    def user_obj_permission(self, user_id: int) -> bool:
        """Проверяет, имеет ли пользователь право на операцию над моделью."""
        return self.warehouse.user_obj_permission(user_id)
