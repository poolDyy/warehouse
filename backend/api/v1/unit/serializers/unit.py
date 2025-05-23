from rest_framework import serializers

from apps.unit.models import Unit, UnitGroup
from apps.unit.services import UnitTranslationService


class UnitGroupSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = UnitGroup
        fields = [
            'id',
            'title',
        ]

    def get_title(self, obj: UnitGroup) -> str:
        translation = UnitTranslationService.get_unit_group_translation(
            group=obj,
        )
        return translation.title


class UnitSerializer(serializers.ModelSerializer):
    group = UnitGroupSerializer()

    title = serializers.SerializerMethodField()
    short_title = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = [
            'id',
            'coefficient',
            'group',
            'title',
            'short_title',
        ]

    def get_title(self, obj: Unit) -> str:
        translation = UnitTranslationService.get_unit_translation(unit=obj)
        return translation.title

    def get_short_title(self, obj: Unit) -> str:
        translation = UnitTranslationService.get_unit_translation(unit=obj)
        return translation.short_title
