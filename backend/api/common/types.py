from typing import Type

from attr import dataclass
from rest_framework.serializers import Serializer


@dataclass(frozen=True)
class SerializerTypeMapping:
    """Описывает типы сериализатора."""

    response: Type[Serializer]
    request: Type[Serializer] | None = None


@dataclass(frozen=True)
class SerializerMapping:
    """Описывает структуру атрибута serializer в SerializerViewSetMixin."""

    list: SerializerTypeMapping | None = None
    retrieve: SerializerTypeMapping | None = None
    create: SerializerTypeMapping | None = None
    update: SerializerTypeMapping | None = None
    partial_update: SerializerTypeMapping | None = None
    delete: SerializerTypeMapping | None = None
    actions: dict[str:SerializerTypeMapping] = {}
