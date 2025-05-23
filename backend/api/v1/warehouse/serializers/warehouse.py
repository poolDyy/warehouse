from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.common.serializers import BaseSerializer
from api.v1.warehouse.serializers.common import WarehouseAttachmentsModelsSerializer, WareHouseCategoriesSerializer
from apps.warehouse.choices import StorageTypeChoices
from apps.warehouse.models import Material, Product, Warehouse


class WarehouseResponseModelSerializer(BaseSerializer):
    categories = WareHouseCategoriesSerializer(many=True, required=False)
    attachments = WarehouseAttachmentsModelsSerializer(many=True, required=False)
    materials_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    storage_type = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = [
            'id',
            'title',
            'storage_type',
            'user',
            'materials_count',
            'products_count',
            'categories',
            'attachments',
        ]
        read_only_fields = fields

    def get_materials_count(self, obj: Warehouse) -> str:
        if obj.storage_type == StorageTypeChoices.MATERIAL:
            return Material.objects.filter(warehouse_id=obj.id).count()
        return '-'

    def get_products_count(self, obj: Warehouse) -> str:
        if obj.storage_type == StorageTypeChoices.PRODUCT:
            return Product.objects.filter(warehouse_id=obj.id).count()
        return '-'

    @extend_schema_field(
        {
            'type': 'object',
            'properties': {
                'value': {'type': 'string'},
                'label': {'type': 'string'},
            },
            'required': ['value', 'label'],
        }
    )
    def get_storage_type(self, obj: Warehouse) -> dict:
        choices = dict(StorageTypeChoices.choices)
        return {
            'value': obj.storage_type,
            'label': choices.get(obj.storage_type, str(obj.storage_type)),
        }


class WarehouseCreateModelSerializer(BaseSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'id',
            'title',
            'storage_type',
            'categories',
        ]


class WarehouseUpdateModelSerializer(BaseSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'id',
            'title',
            'storage_type',
            'categories',
        ]
