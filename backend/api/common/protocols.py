from typing import Protocol


class UserObjPermissionProtocol(Protocol):
    """Протокол объектов с ограниченным доступом юзеров."""

    def user_obj_permission(self, user_id: int) -> bool: ...
