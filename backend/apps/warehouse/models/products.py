from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from .abs_storage_entity import StorageEntity


class Product(StorageEntity):
    """Продукты."""

    components = GenericRelation(
        'warehouse.ProductComponent',
        related_query_name='products',
    )

    attachments = GenericRelation(
        'warehouse.FileAttachment',
        related_query_name='products',
    )

    warehouse = models.ForeignKey(
        verbose_name=_('Склад'),
        to='warehouse.Warehouse',
        on_delete=models.CASCADE,
        related_name='products',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
        indexes = [
            models.Index(fields=['warehouse']),
            models.Index(fields=['unit']),
        ]

    def user_obj_permission(self, user_id: int) -> bool:
        """Проверяет, имеет ли пользователь право на операцию над моделью."""
        return self.warehouse.user_obj_permission(user_id)
