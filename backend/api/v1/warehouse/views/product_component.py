from functools import cached_property

from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.common.permissions import HasUserObjPerms
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseModelViewSet
from api.v1.warehouse.serializers import (
    ProductComponentCreateSerializer,
    ProductComponentResponseSerializer,
    ProductComponentUpdateSerializer,
)
from apps.warehouse.models import Product, ProductComponent
from apps.warehouse.services.product_component import ProductComponentCreateService, ProductComponentUpdateService


class ProductComponentViewSet(BaseModelViewSet):
    """ViewSet CRUD компонентов продукта."""

    permission_classes = [IsAuthenticated, HasUserObjPerms]
    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=ProductComponentResponseSerializer,
            request=ProductComponentResponseSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=ProductComponentResponseSerializer,
            request=ProductComponentResponseSerializer,
        ),
        create=SerializerTypeMapping(
            response=ProductComponentResponseSerializer,
            request=ProductComponentCreateSerializer,
        ),
        update=SerializerTypeMapping(
            response=ProductComponentResponseSerializer,
            request=ProductComponentUpdateSerializer,
        ),
    )

    @cached_property
    def product(self) -> Product:
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        self.check_object_permissions(self.request, product)
        return product

    def get_queryset(self) -> QuerySet[ProductComponent]:
        return (
            ProductComponent.objects.select_related(
                'product',
                'unit',
                'unit__group',
                'content_type',
            )
            .prefetch_related(
                'unit__translations',
            )
            .filter(product=self.product)
        )

    def perform_create(self, serializer: ProductComponentCreateSerializer) -> ProductComponent:
        validated_data = serializer.validated_data
        service = ProductComponentCreateService(
            product=self.product,
            unit=validated_data.get('unit'),
            content_type=validated_data.get('content_type'),
            object_id=validated_data.get('object_id'),
            quantity=validated_data.get('quantity'),
            user_id=self.request.user.id,
        )
        return service.create()

    def perform_update(self, serializer: ProductComponentUpdateSerializer) -> ProductComponent:
        validated_data = serializer.validated_data
        instance = serializer.instance

        service = ProductComponentUpdateService(
            id=instance.id,
            product=self.product,
            unit=validated_data.get('unit'),
            content_type=validated_data.get('content_type'),
            object_id=validated_data.get('object_id'),
            quantity=validated_data.get('quantity'),
            user_id=self.request.user.id,
        )
        return service.update(instance)
