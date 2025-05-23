import dataclasses
from decimal import Decimal
from functools import cached_property

from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.unit.models import Unit
from apps.warehouse.choices import CategoryTypeChoices, StorageTypeChoices
from apps.warehouse.models import Category, Material, Warehouse
from apps.warehouse.validators.category import category_type_validate, warehouse_category_and_entity_validate


@dataclasses.dataclass
class MaterialService:
    """Сервис по созданию и обновлению материалов склада."""

    warehouse: Warehouse
    unit: Unit

    title: str
    sku: str
    notes: str
    price: Decimal
    remaining: Decimal
    min_remaining: Decimal

    categories_id: list[int] = lambda: []

    def create(self) -> Material:
        self.validate()

        with transaction.atomic():
            material = Material.objects.create(
                warehouse=self.warehouse,
                unit=self.unit,
                title=self.title,
                sku=self.sku,
                notes=self.notes,
                price=self.price,
                remaining=self.remaining,
                min_remaining=self.min_remaining,
            )

            material.categories.set(self.categories_qs)

        return material

    def update(self, material: Material) -> Material:
        self.validate()

        with transaction.atomic():
            material.unit = self.unit
            material.title = self.title
            material.sku = self.sku
            material.notes = self.notes
            material.price = self.price
            material.remaining = self.remaining
            material.min_remaining = self.min_remaining

            material.save()
            material.categories.set(self.categories_qs)

        return material

    def validate(self) -> None:
        if self.warehouse.storage_type != StorageTypeChoices.MATERIAL:
            raise serializers.ValidationError({'warehouse': _('Склад не предназначен для материалов')})

        if self.categories_qs:
            warehouse_category_and_entity_validate(
                warehouse=self.warehouse,
                entity_categories=self.categories_qs,
            )
            category_type_validate(
                categories=self.categories_qs,
                category_type=CategoryTypeChoices.MATERIAL,
            )

    @cached_property
    def categories_qs(self) -> QuerySet[Category]:
        return Category.objects.filter(id__in=self.categories_id)
