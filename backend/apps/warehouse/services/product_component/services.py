import dataclasses
from decimal import Decimal
from functools import cached_property

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.unit.models import Unit
from apps.warehouse.choices import ProductComponentChoices
from apps.warehouse.models import Material, Product, ProductComponent, Resource

CONTENT_TYPE_MAP: dict[str, ContentType] = {
    ProductComponentChoices.MATERIAL: ContentType.objects.get_for_model(Material),
    ProductComponentChoices.RESOURCE: ContentType.objects.get_for_model(Resource),
}


@dataclasses.dataclass
class ProductComponentBaseService:
    product: Product
    unit: Unit

    content_type: str | ContentType
    object_id: int
    quantity: Decimal
    user_id: int
    id: int | None = None

    @property
    def content_type_instance(self) -> ContentType:
        if isinstance(self.content_type, str):
            return CONTENT_TYPE_MAP[self.content_type]
        if isinstance(self.content_type, ContentType):
            return self.content_type
        raise ValueError(f'Невалидный content_type {self.content_type}')

    @cached_property
    def component_instance(self) -> Material | Resource:
        component_model = self.content_type_instance.model_class()
        try:
            instance = component_model.objects.select_related(
                'unit',
            ).get(id=self.object_id)
        except component_model.DoesNotExist:
            raise serializers.ValidationError({'object_id': _('Объект не найден')})
        return instance

    def validate(self) -> None:
        if self.quantity < 0:
            raise serializers.ValidationError({'quantity': _('Количество должно быть положительным')})

        if not self.component_instance.user_obj_permission(self.user_id):
            raise serializers.ValidationError({'content_type': _('Компонент не принадлежит пользователю')})

        if self.unit.group_id != self.component_instance.unit.group_id:
            raise serializers.ValidationError({'unit': _('Выбрана единица измерения не соответсвующая продукту')})

        if (
            ProductComponent.objects.filter(
                product=self.product,
                content_type=self.content_type_instance,
                object_id=self.object_id,
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise serializers.ValidationError({'object_id': _('Компонент уже находится в составе продукта')})


@dataclasses.dataclass
class ProductComponentCreateService(ProductComponentBaseService):
    def create(self) -> ProductComponent:
        self.validate()
        return ProductComponent.objects.create(
            product=self.product,
            unit=self.unit,
            quantity=self.quantity,
            content_type=self.content_type_instance,
            object_id=self.object_id,
        )


@dataclasses.dataclass
class ProductComponentUpdateService(ProductComponentBaseService):
    def update(self, instance: ProductComponent) -> ProductComponent:
        self.validate()

        instance.quantity = self.quantity
        instance.unit = self.unit
        instance.content_type = self.content_type_instance
        instance.object_id = self.object_id

        instance.save()

        return instance
