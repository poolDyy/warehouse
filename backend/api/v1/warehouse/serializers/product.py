from rest_framework import serializers

from api.v1.warehouse.serializers.common import (
    StorageEntityRequestSerializer,
    StorageEntityResponseSerializer,
    WarehouseAttachmentsModelsSerializer,
)
from apps.warehouse.models import Product

from .product_component import (
    ProductComponentCreateSerializer,
    ProductComponentResponseSerializer,
    ProductComponentUpdateSerializer,
)


class ProductCreateSerializer(StorageEntityRequestSerializer):
    components = ProductComponentCreateSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'components',
        ] + StorageEntityRequestSerializer.Meta.fields


class ProductComponentForProductUpdateSerializer(ProductComponentUpdateSerializer):
    id = serializers.IntegerField(min_value=1, required=False)


class ProductUpdateSerializer(StorageEntityRequestSerializer):
    components = ProductComponentForProductUpdateSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'components',
        ] + StorageEntityRequestSerializer.Meta.fields


class ProductDetailSerializer(StorageEntityResponseSerializer):
    attachments = WarehouseAttachmentsModelsSerializer(many=True, required=False)
    components = ProductComponentResponseSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'warehouse',
            'attachments',
            'components',
        ] + StorageEntityResponseSerializer.Meta.fields


class ProductListSerializer(StorageEntityResponseSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'warehouse',
        ] + StorageEntityResponseSerializer.Meta.fields
