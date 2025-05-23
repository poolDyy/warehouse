from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    'CategoryTypeChoices',
    'StorageTypeChoices',
    'ContentTypeChoices',
    'ProductComponentChoices',
]


class CategoryTypeChoices(models.TextChoices):
    """Типы категорий."""

    PRODUCT = 'product', _('Продукты')
    MATERIAL = 'material', _('Материалы')
    RESOURCE = 'resource', _('Ресурсы')


class StorageTypeChoices(models.TextChoices):
    """Типы складов."""

    MATERIAL = 'material', _('Материалы')
    PRODUCT = 'product', _('Продукты')


class ContentTypeChoices(models.TextChoices):
    """ContentType для моделей, к которым можно прикрепить файл."""

    PRODUCT = 'product', _('Продукты')
    MATERIAL = 'material', _('Материалы')
    RESOURCE = 'resource', _('Ресурсы')
    WAREHOUSE = 'warehouse', _('Склад')


class ProductComponentChoices(models.TextChoices):
    """ContentType для моделей относящихся к компонентам продукта."""

    MATERIAL = 'material', _('Материалы')
    RESOURCE = 'resource', _('Ресурсы')
