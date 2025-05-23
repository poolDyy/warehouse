from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

__all__ = ['StorageEntity']


class StorageEntity(BaseModel):
    """Общая модель для объектов хранимых на складе."""

    categories = models.ManyToManyField(
        verbose_name=_('Категории'),
        to='warehouse.Category',
    )

    unit = models.ForeignKey(
        verbose_name=_('Единица измерения'),
        to='unit.Unit',
        on_delete=models.PROTECT,
    )

    title = models.CharField(
        verbose_name=_('Наименование'),
        max_length=255,
    )

    price = models.DecimalField(
        verbose_name=_('Цена'),
        decimal_places=2,
        max_digits=12,
    )

    notes = models.TextField(
        verbose_name=_('Заметки'),
        blank=True,
        default='',
    )

    remaining = models.DecimalField(
        verbose_name=_('Остаток'),
        decimal_places=4,
        max_digits=12,
        default=0,
    )

    min_remaining = models.DecimalField(
        verbose_name=_('Минимальный остаток'),
        decimal_places=4,
        max_digits=12,
        null=True,
    )

    sku = models.CharField(
        verbose_name='SKU',
        max_length=255,
        blank=True,
        default='',
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title
