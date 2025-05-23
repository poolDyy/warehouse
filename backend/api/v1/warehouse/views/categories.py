from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated

from api.common.permissions import HasUserObjPerms
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseModelViewSet
from api.v1.warehouse.serializers import CategoryCreateSerializer, CategoryResponseSerializer
from api.v1.warehouse.serializers.categories import CategoryUpdateSerializer
from apps.warehouse.models import Category


class CategoryViewSet(BaseModelViewSet):
    """ViewSet CRUD категорий."""

    permission_classes = [IsAuthenticated, HasUserObjPerms]
    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=CategoryResponseSerializer,
            request=CategoryCreateSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=CategoryResponseSerializer,
            request=CategoryResponseSerializer,
        ),
        create=SerializerTypeMapping(
            response=CategoryResponseSerializer,
            request=CategoryCreateSerializer,
        ),
        update=SerializerTypeMapping(
            response=CategoryResponseSerializer,
            request=CategoryUpdateSerializer,
        ),
    )

    def get_queryset(self) -> QuerySet[Category]:
        return Category.objects.select_related('user').filter(user=self.request.user)

    def perform_create(self, serializer: CategoryCreateSerializer) -> Category:
        data = serializer.validated_data
        data['user'] = self.request.user
        return Category.objects.create(**data)
