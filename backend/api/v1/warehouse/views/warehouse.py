from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from api.common.permissions import HasUserObjPerms
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseModelViewSet
from api.v1.warehouse.serializers import (
    WarehouseCreateModelSerializer,
    WarehouseResponseModelSerializer,
    WarehouseUpdateModelSerializer,
)
from apps.warehouse.models import Warehouse
from apps.warehouse.services.warehouse import WarehouseService


class WarehouseViewSet(BaseModelViewSet):
    """ViewSet CRUD склада."""

    permission_classes = [IsAuthenticated, HasUserObjPerms]
    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=WarehouseResponseModelSerializer,
            request=WarehouseResponseModelSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=WarehouseResponseModelSerializer,
            request=WarehouseResponseModelSerializer,
        ),
        create=SerializerTypeMapping(
            response=WarehouseResponseModelSerializer,
            request=WarehouseCreateModelSerializer,
        ),
        update=SerializerTypeMapping(
            response=WarehouseResponseModelSerializer,
            request=WarehouseUpdateModelSerializer,
        ),
    )

    def get_queryset(self) -> QuerySet[Warehouse]:
        return (
            Warehouse.objects.select_related('user')
            .prefetch_related('categories', 'attachments')
            .filter(user=self.request.user)
        )

    def perform_create(self, serializer: Serializer) -> Warehouse:
        validated_data = serializer.validated_data

        service = WarehouseService(
            title=validated_data['title'],
            user_id=self.request.user.id,
            storage_type=validated_data['storage_type'],
            categories_id=[category.id for category in validated_data.get('categories', [])],
        )

        return service.create()

    def perform_update(self, serializer: Serializer) -> Warehouse:
        validated_data = serializer.validated_data
        instance = serializer.instance

        service = WarehouseService(
            title=validated_data['title'],
            user_id=self.request.user.id,
            storage_type=validated_data['storage_type'],
            categories_id=[category.id for category in validated_data.get('categories', [])],
        )

        return service.update(instance)
