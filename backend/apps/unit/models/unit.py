from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models.choices import LanguageChoices


class Unit(models.Model):
    """Модель единицы измерения."""

    coefficient = models.DecimalField(
        verbose_name=_('Коэфф. приведения'),
        max_digits=10,
        decimal_places=6,
    )
    group = models.ForeignKey(
        to='unit.UnitGroup',
        related_name='units',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['group', 'coefficient']
        verbose_name = _('Ед. измерений')
        verbose_name_plural = _('Ед. измерений')
        indexes = [
            models.Index(fields=['group']),
        ]

    def __str__(self) -> str:
        return f'Ед. измерения: {self.id}'


class UnitTranslation(models.Model):
    """Переводы для единиц измерения."""

    unit = models.ForeignKey(
        verbose_name=_('Единица измерения'),
        to=Unit,
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
        max_length=100,
    )

    short_title = models.CharField(
        verbose_name=_('Сокращенное наименование'),
        max_length=20,
    )

    class Meta:
        ordering = ('unit', 'language_code')
        unique_together = ('unit', 'language_code')
        verbose_name = _('Перевод ед. измерений')
        verbose_name_plural = _('Переводы ед. измерений')
        indexes = [
            models.Index(fields=['unit', 'language_code']),
            models.Index(fields=['unit']),
        ]

    def __str__(self) -> str:
        return f'{self.title} ({self.short_title}, {self.language_code})'
