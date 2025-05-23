from api.common.serializers import BaseSerializer
from api.v1.warehouse.serializers.common import (
    WarehouseAttachmentsModelsSerializer,
    WareHouseCategoriesSerializer,
    WarehouseUnitSerializer,
)
from apps.warehouse.models import Resource


class ResourceResponseSerializer(BaseSerializer):
    attachments = WarehouseAttachmentsModelsSerializer(
        many=True,
        required=False,
    )
    categories = WareHouseCategoriesSerializer(
        many=True,
        required=False,
    )
    unit = WarehouseUnitSerializer(read_only=True)

    class Meta:
        model = Resource
        fields = [
            'id',
            'title',
            'notes',
            'is_depreciation',
            'price',
            'initial_price',
            'service_life',
            'user',
            'unit',
            'attachments',
            'categories',
        ]


class ResourceCreateSerializer(BaseSerializer):
    class Meta:
        model = Resource
        fields = [
            'id',
            'title',
            'notes',
            'is_depreciation',
            'price',
            'initial_price',
            'service_life',
            'unit',
            'categories',
        ]


class ResourceUpdateSerializer(BaseSerializer):
    class Meta:
        model = Resource
        fields = [
            'id',
            'title',
            'notes',
            'is_depreciation',
            'price',
            'initial_price',
            'service_life',
            'unit',
            'categories',
        ]
