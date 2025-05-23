from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Resource(BaseModel):
    """Ресурсы."""

    attachments = GenericRelation(
        'warehouse.FileAttachment',
        related_query_name='resource',
    )

    categories = models.ManyToManyField(
        verbose_name=_('Категории'),
        to='warehouse.Category',
        related_name='resources',
    )

    user = models.ForeignKey(
        verbose_name=_('Пользователь'),
        to='users.User',
        on_delete=models.CASCADE,
        related_name='resources',
    )

    unit = models.ForeignKey(
        verbose_name=_('Единица измерения'),
        to='unit.Unit',
        on_delete=models.PROTECT,
        related_name='resources',
    )

    title = models.CharField(
        verbose_name=_('Наименование'),
        max_length=255,
    )

    is_depreciation = models.BooleanField(
        verbose_name=_('Амортизация'),
        default=False,
    )

    price = models.DecimalField(
        verbose_name=_('Цена'),
        decimal_places=2,
        max_digits=12,
        null=True,
    )

    initial_price = models.DecimalField(
        verbose_name=_('Первоначальная стоимость'),
        decimal_places=2,
        max_digits=12,
        null=True,
    )

    service_life = models.DecimalField(
        verbose_name=_('Срок службы'),
        decimal_places=4,
        max_digits=12,
        null=True,
    )

    notes = models.TextField(
        verbose_name=_('Заметки'),
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = _('Ресурс')
        verbose_name_plural = _('Ресурсы')
        indexes = [
            models.Index(fields=['unit']),
            models.Index(fields=['user']),
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    # Если is_depreciation = False: price NOT NULL, initial_price и service_life NULL
                    Q(is_depreciation=False, price__isnull=False, initial_price__isnull=True, service_life__isnull=True)
                    |
                    # Если is_depreciation = True: price NULL, initial_price и service_life NOT NULL
                    Q(is_depreciation=True, price__isnull=True, initial_price__isnull=False, service_life__isnull=False)
                ),
                name='resource_depreciation_constraint',
            )
        ]

    def __str__(self) -> str:
        return self.title

    def user_obj_permission(self, user_id: int) -> bool:
        """Проверяет, имеет ли пользователь право на операцию над моделью."""
        return self.user_id == user_id
