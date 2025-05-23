from rest_framework import serializers

from api.common.serializers import BaseSerializer
from apps.unit.models import Unit
from apps.unit.services import UnitTranslationService
from apps.warehouse.models import Category, FileAttachment
from apps.warehouse.models.abs_storage_entity import StorageEntity


class WarehouseAttachmentsModelsSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FileAttachment
        fields = [
            'id',
            'file_name',
        ]

    def get_file_name(self, obj: FileAttachment) -> str:
        return obj.file.name.split('/')[-1] if obj.file.name else None


class WarehouseUnitSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_title = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = [
            'id',
            'title',
            'short_title',
        ]

    def get_title(self, obj: Unit) -> str:
        translation = UnitTranslationService.get_unit_translation(unit=obj)
        return translation.title

    def get_short_title(self, obj: Unit) -> str:
        translation = UnitTranslationService.get_unit_translation(unit=obj)
        return translation.short_title


class WareHouseCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'category_type',
        ]
        read_only_fields = fields


class StorageEntityRequestSerializer(BaseSerializer):
    class Meta:
        model = StorageEntity
        fields = [
            'categories',
            'unit',
            'title',
            'price',
            'notes',
            'remaining',
            'min_remaining',
            'sku',
        ]


class StorageEntityResponseSerializer(BaseSerializer):
    unit = WarehouseUnitSerializer(read_only=True)
    categories = WareHouseCategoriesSerializer(many=True, required=False)

    class Meta:
        model = StorageEntity
        fields = [
            'categories',
            'unit',
            'title',
            'price',
            'notes',
            'remaining',
            'min_remaining',
            'sku',
        ]
        read_only_fields = fields
