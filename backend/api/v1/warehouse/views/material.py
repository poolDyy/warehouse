from functools import cached_property

from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.common.permissions import HasUserObjPerms
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseModelViewSet
from api.v1.warehouse.serializers import MaterialCreateSerializer, MaterialResponseSerializer, MaterialUpdateSerializer
from apps.warehouse.models import Material, Warehouse
from apps.warehouse.services.material.service import MaterialService


class MaterialViewSet(BaseModelViewSet):
    """ViewSet CRUD материалов."""

    permission_classes = [IsAuthenticated, HasUserObjPerms]
    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=MaterialResponseSerializer,
            request=MaterialResponseSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=MaterialResponseSerializer,
            request=MaterialResponseSerializer,
        ),
        create=SerializerTypeMapping(
            response=MaterialResponseSerializer,
            request=MaterialCreateSerializer,
        ),
        update=SerializerTypeMapping(
            response=MaterialResponseSerializer,
            request=MaterialUpdateSerializer,
        ),
    )

    @cached_property
    def warehouse(self) -> Warehouse:
        warehouse_id = self.kwargs.get('warehouse_id')
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
        self.check_object_permissions(self.request, warehouse)
        return warehouse

    def get_queryset(self) -> QuerySet[Material]:
        return (
            Material.objects.select_related(
                'warehouse',
                'unit',
            )
            .prefetch_related(
                'attachments',
                'categories',
                'unit__translations',
            )
            .filter(warehouse=self.warehouse)
        )

    def perform_create(self, serializer: MaterialCreateSerializer) -> Material:
        validated_data = serializer.validated_data
        service = MaterialService(
            warehouse=self.warehouse,
            unit=validated_data['unit'],
            title=validated_data['title'],
            sku=validated_data['sku'],
            notes=validated_data['notes'],
            price=validated_data['price'],
            remaining=validated_data['remaining'],
            min_remaining=validated_data['min_remaining'],
            categories_id=[category.id for category in validated_data.get('categories', [])],
        )

        return service.create()

    def perform_update(self, serializer: MaterialUpdateSerializer) -> Material:
        validated_data = serializer.validated_data
        instance = serializer.instance

        service = MaterialService(
            warehouse=self.warehouse,
            unit=validated_data['unit'],
            title=validated_data['title'],
            sku=validated_data['sku'],
            notes=validated_data['notes'],
            price=validated_data['price'],
            remaining=validated_data['remaining'],
            min_remaining=validated_data['min_remaining'],
            categories_id=[category.id for category in validated_data.get('categories', [])],
        )

        return service.update(instance)
