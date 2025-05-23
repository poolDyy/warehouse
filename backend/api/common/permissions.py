from typing import Type

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from api.common.protocols import UserObjPermissionProtocol

__all__ = [
    'IsUnauthenticated',
    'HasUserObjPerms',
]


class IsUnauthenticated(BasePermission):
    """Разрешение для неавторизованных пользователей."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        return not request.user.is_authenticated


class HasUserObjPerms(BasePermission):
    """Проверяет права пользователя на объект модели."""

    def has_object_permission(self, request: Request, view: Type[ViewSet], obj: UserObjPermissionProtocol) -> bool:
        return obj.user_obj_permission(request.user.id)
