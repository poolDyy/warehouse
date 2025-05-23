from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.common.serializers import BaseSerializer
from apps.warehouse.choices import CategoryTypeChoices
from apps.warehouse.models import Category


class CategoryCreateSerializer(BaseSerializer):
    class Meta:
        model = Category

        fields = [
            'id',
            'title',
            'category_type',
        ]


class CategoryUpdateSerializer(BaseSerializer):
    class Meta:
        model = Category

        fields = [
            'id',
            'title',
        ]


class CategoryResponseSerializer(BaseSerializer):
    category_type = serializers.SerializerMethodField()

    class Meta:
        model = Category

        fields = [
            'id',
            'user',
            'title',
            'category_type',
        ]

    @extend_schema_field(
        {
            'type': 'object',
            'properties': {
                'value': {'type': 'string'},
                'label': {'type': 'string'},
            },
            'required': ['value', 'label'],
        }
    )
    def get_category_type(self, obj: Category) -> dict:
        choices = dict(CategoryTypeChoices.choices)
        return {
            'value': obj.category_type,
            'label': choices.get(obj.category_type, str(obj.category_type)),
        }
