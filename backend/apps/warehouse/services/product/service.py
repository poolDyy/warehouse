import dataclasses
from collections import defaultdict
from decimal import Decimal
from functools import cached_property

from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.unit.models import Unit
from apps.warehouse.choices import CategoryTypeChoices, StorageTypeChoices
from apps.warehouse.models import Category, Product, ProductComponent, Warehouse
from apps.warehouse.services.dto import ProductComponentDTO
from apps.warehouse.services.product_component import ProductComponentCreateService, ProductComponentUpdateService
from apps.warehouse.validators.category import category_type_validate, warehouse_category_and_entity_validate


@dataclasses.dataclass
class ProductBaseService:
    unit: Unit
    warehouse: Warehouse

    title: str
    sku: str
    notes: str
    price: Decimal
    remaining: Decimal
    min_remaining: Decimal

    categories_id: list[int]
    components: list[ProductComponentDTO]

    @cached_property
    def categories_qs(self) -> QuerySet[Category]:
        return Category.objects.filter(id__in=self.categories_id)

    def validate(self) -> None:
        if self.warehouse.storage_type != StorageTypeChoices.PRODUCT:
            raise serializers.ValidationError({'warehouse': _('Склад не предназначен для продуктов')})
        if self.categories_qs:
            warehouse_category_and_entity_validate(
                warehouse=self.warehouse,
                entity_categories=self.categories_qs,
            )
            category_type_validate(
                categories=self.categories_qs,
                category_type=CategoryTypeChoices.PRODUCT,
            )


@dataclasses.dataclass
class ProductCreateService(ProductBaseService):
    def create(self) -> Product:
        self.validate()

        with transaction.atomic():
            product = Product.objects.create(
                warehouse=self.warehouse,
                unit=self.unit,
                title=self.title,
                sku=self.sku,
                notes=self.notes,
                price=self.price,
                remaining=self.remaining,
                min_remaining=self.min_remaining,
            )

            product.categories.set(self.categories_qs)

            self._create_components(instance=product)

        return product

    def _create_components(self, instance: Product) -> None:
        errors = defaultdict(lambda: dict())
        for i, component in enumerate(self.components):
            service = ProductComponentCreateService(
                product=instance,
                unit=component.unit,
                content_type=component.content_type,
                object_id=component.object_id,
                quantity=component.quantity,
                user_id=component.user_id,
            )
            try:
                service.create()
            except serializers.ValidationError as e:
                errors['components'][i] = e.detail
        if errors:
            raise serializers.ValidationError(errors)


@dataclasses.dataclass
class ProductUpdateService(ProductBaseService):
    @cached_property
    def product_components(self) -> dict[int, ProductComponent]:
        ids = [component.id for component in self.components]
        components = ProductComponent.objects.select_related('product', 'content_type', 'unit').filter(id__in=ids)
        return {product.id: product for product in components}

    def update(self, instance: Product) -> Product:
        self.validate()
        with transaction.atomic():
            instance.title = self.title
            instance.unit = self.unit

            instance.sku = self.sku
            instance.notes = self.notes
            instance.price = self.price
            instance.min_remaining = self.min_remaining
            instance.remaining = self.remaining

            instance.save()

            instance.categories.set(self.categories_qs)
            self._components_changes(instance=instance)

        return instance

    def _components_changes(self, instance: Product) -> None:
        errors = defaultdict(lambda: dict())
        for i, component in enumerate(self.components):
            model_instance = self.product_components.get(component.id)
            try:
                if model_instance:
                    self._update_component(
                        product_model_instance=instance,
                        component_model_instance=model_instance,
                        component_dto=component,
                    )
                else:
                    self._create_component(
                        product_model_instance=instance,
                        component_dto=component,
                    )
            except serializers.ValidationError as e:
                errors['components'][i] = e.detail
        if errors:
            raise serializers.ValidationError(errors)

    @classmethod
    def _update_component(
        cls,
        product_model_instance: Product,
        component_model_instance: ProductComponent,
        component_dto: ProductComponentDTO,
    ) -> None:
        service = ProductComponentUpdateService(
            id=component_dto.id,
            product=product_model_instance,
            unit=component_dto.unit,
            content_type=component_dto.content_type,
            object_id=component_dto.object_id,
            quantity=component_dto.quantity,
            user_id=component_dto.user_id,
        )
        service.update(instance=component_model_instance)

    @classmethod
    def _create_component(
        cls,
        product_model_instance: Product,
        component_dto: ProductComponentDTO,
    ) -> None:
        service = ProductComponentCreateService(
            product=product_model_instance,
            unit=component_dto.unit,
            content_type=component_dto.content_type,
            object_id=component_dto.object_id,
            quantity=component_dto.quantity,
            user_id=component_dto.user_id,
        )
        service.create()
