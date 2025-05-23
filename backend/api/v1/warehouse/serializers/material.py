from rest_framework import serializers

from api.v1.warehouse.serializers.common import (
    StorageEntityRequestSerializer,
    StorageEntityResponseSerializer,
    WarehouseAttachmentsModelsSerializer,
)
from apps.warehouse.models import Material, Warehouse


class MaterialWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'id',
            'title',
        ]


class MaterialCreateSerializer(StorageEntityRequestSerializer):
    class Meta:
        model = Material
        fields = [
            'id',
        ] + StorageEntityRequestSerializer.Meta.fields


class MaterialUpdateSerializer(StorageEntityRequestSerializer):
    class Meta:
        model = Material
        fields = [
            'id',
        ] + StorageEntityRequestSerializer.Meta.fields


class MaterialResponseSerializer(StorageEntityResponseSerializer):
    attachments = WarehouseAttachmentsModelsSerializer(many=True, required=False)
    warehouse = MaterialWarehouseSerializer()

    class Meta:
        model = Material
        fields = [
            'id',
            'warehouse',
            'attachments',
        ] + StorageEntityResponseSerializer.Meta.fields
