import dataclasses
from functools import cached_property

from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.warehouse.choices import CategoryTypeChoices, StorageTypeChoices
from apps.warehouse.models import Category, Warehouse
from apps.warehouse.services.dto import AttachmentsDTO


@dataclasses.dataclass
class WarehouseService:
    """Сервис по созданию и обновлению склада."""

    title: str
    user_id: int
    storage_type: str
    categories_id: list[int] | None = None
    attachments: list[AttachmentsDTO] | None = None

    @cached_property
    def categories_qs(self) -> QuerySet[Category]:
        return Category.objects.filter(id__in=self.categories_id)

    def create(self) -> Warehouse:
        self.validate()
        with transaction.atomic():
            warehouse = Warehouse.objects.create(
                title=self.title,
                user_id=self.user_id,
                storage_type=self.storage_type,
                updated_by_id=self.user_id,
            )

            warehouse.categories.set(self.categories_qs)

        return warehouse

    def update(self, instance: Warehouse) -> Warehouse:
        self.validate()

        with transaction.atomic():
            instance.title = self.title
            instance.storage_type = self.storage_type
            instance.updated_by_id = self.user_id
            instance.save()

            instance.categories.set(self.categories_qs)

        return instance

    def validate(self) -> None:
        # невалдиный тип
        if not any(self.storage_type == choice[0] for choice in StorageTypeChoices.choices):
            raise serializers.ValidationError({'storage_type': _('Недопустимый тип')})

        # Категории могут быть с типом ресурсов м переданного типа
        categories_another_type = self.categories_qs.exclude(
            category_type__in=[self.storage_type, CategoryTypeChoices.RESOURCE]
        )
        if categories_another_type.count() > 0:
            categories_titles = ', '.join(categories_another_type.values_list('title', flat=True))
            raise serializers.ValidationError(
                {
                    'categories': _('Категории не подходят под тип склада: ') + categories_titles,
                },
            )
