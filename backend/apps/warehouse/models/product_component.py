from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductComponent(models.Model):
    product = models.ForeignKey(
        verbose_name='Продукт',
        to='warehouse.Product',
        on_delete=models.CASCADE,
        related_name='components',
    )

    quantity = models.DecimalField(
        verbose_name='Количество',
        max_digits=10,
        decimal_places=2,
    )

    unit = models.ForeignKey(
        verbose_name=_('Единица измерения'),
        to='unit.Unit',
        on_delete=models.PROTECT,
    )

    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ['material', 'resource']},
    )
    object_id = models.PositiveIntegerField()
    component = GenericForeignKey(
        'content_type',
        'object_id',
    )

    class Meta:
        unique_together = (
            'product',
            'content_type',
            'object_id',
        )
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self) -> str:
        return f'{self.product.title} - {self.component} ({self.quantity})'

    def user_obj_permission(self, user_id: int) -> bool:
        """Проверяет, имеет ли пользователь право на операцию над моделью."""
        return self.product.user_obj_permission(user_id)
