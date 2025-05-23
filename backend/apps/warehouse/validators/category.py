from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User
from apps.warehouse.models import Category, Warehouse


def warehouse_category_and_entity_validate(
    warehouse: Warehouse,
    entity_categories: QuerySet[Category],
) -> None:
    warehouse_categories = warehouse.categories.values_list('id', flat=True)
    wrong_categories = entity_categories.exclude(id__in=warehouse_categories).values_list(
        'title',
        flat=True,
    )
    if wrong_categories:
        warehouse_categories_titles = ', '.join(wrong_categories)
        raise serializers.ValidationError(
            {'categories': _('Исключите категории не принадлежащие складу: ') + warehouse_categories_titles}
        )


def category_type_validate(
    categories: QuerySet[Category],
    category_type: str,
) -> None:
    categories_another_type = categories.exclude(category_type=category_type)
    if categories_another_type.count() > 0:
        categories_titles = ', '.join(categories_another_type.values_list('title', flat=True))
        raise serializers.ValidationError(
            {
                'categories': _('Категории не соответствуют допустимым типам: ') + categories_titles,
            },
        )


def user_category_validate(
    categories: QuerySet[Category],
    user: User,
) -> None:
    user_categories = Category.objects.filter(user=user).values_list('id', flat=True)
    wrong_categories = categories.exclude(id__in=user_categories).values_list(
        'title',
        flat=True,
    )
    if wrong_categories:
        user_categories_titles = ', '.join(wrong_categories)
        raise serializers.ValidationError(
            {'categories': _('Исключите категории не принадлежащие пользователю: ') + user_categories_titles}
        )
