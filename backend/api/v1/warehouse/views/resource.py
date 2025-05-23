from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated

from api.common.permissions import HasUserObjPerms
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseModelViewSet
from api.v1.warehouse.serializers import (
    ResourceCreateSerializer,
    ResourceResponseSerializer,
    ResourceUpdateSerializer,
)
from apps.warehouse.models import Material, Resource
from apps.warehouse.services.resource.service import ResourceService


class ResourceViewSet(BaseModelViewSet):
    """ViewSet CRUD ресурсов."""

    permission_classes = [IsAuthenticated, HasUserObjPerms]
    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=ResourceResponseSerializer,
            request=ResourceResponseSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=ResourceResponseSerializer,
            request=ResourceResponseSerializer,
        ),
        create=SerializerTypeMapping(
            response=ResourceResponseSerializer,
            request=ResourceCreateSerializer,
        ),
        update=SerializerTypeMapping(
            response=ResourceResponseSerializer,
            request=ResourceUpdateSerializer,
        ),
    )

    def get_queryset(self) -> QuerySet[Material]:
        return (
            Resource.objects.select_related(
                'unit',
                'user',
            )
            .prefetch_related(
                'attachments',
                'categories',
                'unit__translations',
            )
            .filter(user=self.request.user)
        )

    def perform_create(self, serializer: ResourceCreateSerializer) -> Resource:
        validated_data = serializer.validated_data
        service = ResourceService(
            user=self.request.user,
            unit=validated_data['unit'],
            title=validated_data['title'],
            notes=validated_data['notes'],
            is_depreciation=validated_data['is_depreciation'],
            price=validated_data.get('price'),
            initial_price=validated_data.get('initial_price'),
            service_life=validated_data.get('service_life'),
            categories_id=[category.id for category in validated_data.get('categories', [])],
        )

        return service.create()

    def perform_update(self, serializer: ResourceUpdateSerializer) -> Resource:
        validated_data = serializer.validated_data
        instance = serializer.instance

        service = ResourceService(
            user=self.request.user,
            unit=validated_data['unit'],
            title=validated_data['title'],
            notes=validated_data['notes'],
            is_depreciation=validated_data['is_depreciation'],
            price=validated_data.get('price'),
            initial_price=validated_data.get('initial_price'),
            service_life=validated_data.get('service_life'),
            categories_id=[category.id for category in validated_data.get('categories', [])],
        )

        return service.update(instance)
