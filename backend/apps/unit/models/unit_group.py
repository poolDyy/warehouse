from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models.choices import LanguageChoices


class UnitGroupTranslation(models.Model):
    """Переводы для групп единиц измерения."""

    group = models.ForeignKey(
        to='UnitGroup',
        verbose_name=_('Группа ед. изм.'),
        related_name='translations',
        on_delete=models.CASCADE,
    )

    language_code = models.CharField(
        verbose_name=_('Языковая группа'),
        max_length=10,
        choices=LanguageChoices,
    )

    title = models.CharField(
        verbose_name=_('Наименование'),
        max_length=255,
    )

    class Meta:
        ordering = ['group', 'language_code']
        unique_together = ('group', 'language_code')
        verbose_name = _('Перевод группы ед. измерений')
        verbose_name_plural = _('Переводы групп ед. измерений')
        indexes = [
            models.Index(fields=['group', 'language_code']),
            models.Index(fields=['group']),
        ]

    def __str__(self) -> str:
        return f'{self.title}'


class UnitGroup(models.Model):
    """Модель для групп единиц измерения."""

    def __str__(self) -> str:
        return f'Группа ед. измерений {self.id}'
