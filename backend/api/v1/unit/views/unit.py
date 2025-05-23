from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.v1.unit.serializers import UnitSerializer
from apps.unit.models import Unit


class UnitViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = UnitSerializer

    def get_queryset(self) -> QuerySet[Unit]:
        queryset = (
            Unit.objects.select_related('group')
            .prefetch_related(
                'translations',
                'group__translations',
            )
            .all()
        )
        return queryset
