import dataclasses
from decimal import Decimal
from functools import cached_property

from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.unit.models import Unit
from apps.users.models import User
from apps.warehouse.choices import CategoryTypeChoices
from apps.warehouse.models import Category, Resource
from apps.warehouse.validators.category import category_type_validate, user_category_validate


@dataclasses.dataclass
class ResourceService:
    """Сервис по созданию и обновлению ресурсов."""

    user: User
    unit: Unit

    title: str
    notes: str
    is_depreciation: bool
    initial_price: Decimal | None = None
    service_life: Decimal | None = None
    price: Decimal | None = None

    categories_id: list[int] = lambda: []

    def __post_init__(self) -> None:
        # Если is_depreciation = True: price NULL, initial_price и service_life NOT NULL
        # Если is_depreciation = False: price NOT NULL, initial_price и service_life NULL
        if self.is_depreciation:
            self.price = None
        else:
            self.service_life = None
            self.initial_price = None

    def create(self) -> Resource:
        self.validate()

        with transaction.atomic():
            resource = Resource.objects.create(
                user=self.user,
                unit=self.unit,
                title=self.title,
                notes=self.notes,
                is_depreciation=self.is_depreciation,
                price=self.price,
                initial_price=self.initial_price,
                service_life=self.service_life,
                updated_by=self.user,
            )

            resource.categories.set(self.categories_qs)

        return resource

    def update(self, resource: Resource) -> Resource:
        self.validate()

        with transaction.atomic():
            resource.unit = self.unit
            resource.title = self.title
            resource.is_depreciation = self.is_depreciation
            resource.notes = self.notes
            resource.price = self.price
            resource.initial_price = self.initial_price
            resource.service_life = self.service_life
            resource.updated_by = self.user

            resource.save()
            resource.categories.set(self.categories_qs)

        return resource

    def validate(self) -> None:
        if self.is_depreciation and (self.service_life is None or self.initial_price is None):
            raise serializers.ValidationError(
                {'is_depreciation': _('Необходимо передать первоначальную стоимость и срок службы')}
            )
        elif not self.is_depreciation and self.price is None:
            raise serializers.ValidationError({'price': _('Необходимо передать стоимость')})

        if self.categories_qs:
            user_category_validate(categories=self.categories_qs, user=self.user)

            category_type_validate(
                categories=self.categories_qs,
                category_type=CategoryTypeChoices.RESOURCE,
            )

    @cached_property
    def categories_qs(self) -> QuerySet[Category]:
        return Category.objects.filter(id__in=self.categories_id)
