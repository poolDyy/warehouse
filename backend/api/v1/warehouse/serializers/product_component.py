from rest_framework import serializers

from api.v1.warehouse.serializers.common import WarehouseUnitSerializer
from apps.warehouse.choices import ProductComponentChoices
from apps.warehouse.models import Material, ProductComponent, Resource


class ProductComponentCreateSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(
        choices=ProductComponentChoices.choices,
    )
    object_id = serializers.IntegerField(
        min_value=1,
    )

    class Meta:
        model = ProductComponent
        fields = [
            'id',
            'quantity',
            'unit',
            'content_type',
            'object_id',
        ]


class ProductComponentUpdateSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(
        choices=ProductComponentChoices.choices,
    )
    object_id = serializers.IntegerField(
        min_value=1,
    )

    class Meta:
        model = ProductComponent
        fields = [
            'id',
            'quantity',
            'unit',
            'content_type',
            'object_id',
        ]


class ProductComponentResponseSerializer(serializers.ModelSerializer):
    unit = WarehouseUnitSerializer(read_only=True)

    content_type = serializers.SerializerMethodField()

    class Meta:
        model = ProductComponent
        fields = [
            'id',
            'product',
            'unit',
            'quantity',
            'content_type',
            'object_id',
        ]

    def get_content_type(self, obj: ProductComponent) -> str:
        model_class = obj.content_type.model_class()
        if model_class.__name__ == Material.__name__:
            return ProductComponentChoices.MATERIAL
        if model_class.__name__ == Resource.__name__:
            return ProductComponentChoices.RESOURCE
        raise ValueError(f'Передан не валидный content_type: {model_class.__name__}')
