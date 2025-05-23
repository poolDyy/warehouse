from rest_framework import mixins
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

from api.common.permissions import IsUnauthenticated
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseGenericViewSet, ExCreateModelMixin, SerializerViewSetMixin
from api.v1.users.serializers import (
    UserCreateRequestSerializer,
    UserCreateResponseSerializer,
    UserListRetrieveSerializer,
)
from apps.users.models import User


class UserViewSet(
    SerializerViewSetMixin,
    ExCreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    BaseGenericViewSet,
):
    """ViewSet CRUD пользователей."""

    queryset = User.objects.all()

    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=UserListRetrieveSerializer,
            request=UserListRetrieveSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=UserListRetrieveSerializer,
            request=UserListRetrieveSerializer,
        ),
        create=SerializerTypeMapping(
            response=UserCreateResponseSerializer,
            request=UserCreateRequestSerializer,
        ),
    )

    action_permissions = {
        'create': [IsUnauthenticated],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'partial_update': [IsAuthenticated],
        'destroy': [IsAuthenticated],
    }

    def get_permissions(self) -> list[type[BasePermission]]:
        """Определить разрешения для каждого метода."""
        if self.action in self.action_permissions:
            return [permission() for permission in self.action_permissions[self.action]]
        return super().get_permissions()
