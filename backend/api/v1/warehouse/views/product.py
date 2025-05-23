from functools import cached_property

from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.common.permissions import HasUserObjPerms
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseModelViewSet
from api.v1.warehouse.serializers import (
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductUpdateSerializer,
)
from apps.warehouse.models import Product, Warehouse
from apps.warehouse.services.dto import ProductComponentDTO
from apps.warehouse.services.product import ProductCreateService, ProductUpdateService


class ProductViewSet(BaseModelViewSet):
    """ViewSet CRUD продуктов."""

    permission_classes = [IsAuthenticated, HasUserObjPerms]
    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=ProductListSerializer,
            request=ProductListSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=ProductDetailSerializer,
            request=ProductDetailSerializer,
        ),
        create=SerializerTypeMapping(
            response=ProductDetailSerializer,
            request=ProductCreateSerializer,
        ),
        update=SerializerTypeMapping(
            response=ProductDetailSerializer,
            request=ProductUpdateSerializer,
        ),
    )

    @cached_property
    def warehouse(self) -> Warehouse:
        warehouse_id = self.kwargs.get('warehouse_id')
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
        self.check_object_permissions(self.request, warehouse)
        return warehouse

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.select_related(
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

    def perform_create(self, serializer: ProductCreateSerializer) -> Product:
        validated_data = serializer.validated_data
        service = ProductCreateService(
            warehouse=self.warehouse,
            unit=validated_data['unit'],
            title=validated_data['title'],
            sku=validated_data['sku'],
            notes=validated_data['notes'],
            price=validated_data['price'],
            remaining=validated_data['remaining'],
            min_remaining=validated_data['min_remaining'],
            categories_id=[category.id for category in validated_data.get('categories', [])],
            components=self._get_components(validated_data),
        )

        return service.create()

    def perform_update(self, serializer: ProductUpdateSerializer) -> Product:
        validated_data = serializer.validated_data
        instance = serializer.instance

        service = ProductUpdateService(
            warehouse=self.warehouse,
            unit=validated_data['unit'],
            title=validated_data['title'],
            sku=validated_data['sku'],
            notes=validated_data['notes'],
            price=validated_data['price'],
            remaining=validated_data['remaining'],
            min_remaining=validated_data['min_remaining'],
            categories_id=[category.id for category in validated_data.get('categories', [])],
            components=self._get_components(validated_data),
        )

        return service.update(instance)

    def _get_components(self, data: dict) -> list[ProductComponentDTO]:
        components_data = data.get('components', [])
        components_dto = [
            ProductComponentDTO(
                content_type=component.get('content_type'),
                object_id=component.get('object_id'),
                quantity=component.get('quantity'),
                unit=component.get('unit'),
                user_id=self.request.user.id,
                id=component.get('id'),
            )
            for component in components_data
        ]
        return components_dto
