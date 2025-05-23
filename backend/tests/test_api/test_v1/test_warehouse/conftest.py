from decimal import Decimal

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.unit.models import Unit, UnitGroup, UnitTranslation
from apps.warehouse.choices import CategoryTypeChoices, ProductComponentChoices, StorageTypeChoices
from apps.warehouse.models import Category, FileAttachment, Material, Product, ProductComponent, Resource, Warehouse
from tests.conftest import create_user


@pytest.fixture
def another_user(mixer):
    return create_user(mixer, email='anoter_test@user.ru', telegram_user=None)


@pytest.fixture
def categories_list(mixer, auth_user):
    """Фикстура для создания категорий."""
    categories = mixer.cycle(3).blend(
        Category, user=auth_user, category_type=mixer.sequence(*[choice[0] for choice in CategoryTypeChoices.choices])
    )
    return categories


@pytest.fixture
def category_product(mixer, auth_user):
    """Фикстура для создания категории."""
    return mixer.blend(Category, category_type=CategoryTypeChoices.PRODUCT, user=auth_user)


@pytest.fixture
def category_material(mixer, auth_user):
    """Фикстура для создания категории."""
    return mixer.blend(Category, category_type=CategoryTypeChoices.MATERIAL, user=auth_user)


@pytest.fixture
def category_resource(mixer, auth_user):
    """Фикстура для создания категории."""
    return mixer.blend(Category, category_type=CategoryTypeChoices.RESOURCE, user=auth_user)


@pytest.fixture
def category_another_user(mixer, another_user):
    """Категория другого пользователя."""
    return mixer.blend(Category, user=another_user, category_type=CategoryTypeChoices.RESOURCE)


@pytest.fixture
def warehouse(mixer, auth_user, category_product):
    """Фикстура для создания склада."""
    warehouse = mixer.blend(
        Warehouse,
        user=auth_user,
        storage_type=StorageTypeChoices.PRODUCT,
        updated_by=auth_user,
        categories=[],
    )
    warehouse.categories.add(category_product)
    return warehouse


@pytest.fixture
def warehouse_material(mixer, auth_user, category_material):
    """Фикстура для создания склада материалов."""
    warehouse_material = mixer.blend(
        Warehouse,
        user=auth_user,
        storage_type=StorageTypeChoices.MATERIAL,
        updated_by=auth_user,
        categories=[],
    )
    warehouse_material.categories.add(category_material)
    return warehouse_material


@pytest.fixture
def warehouse_another_user(mixer, another_user):
    """Фикстура для создания склада принадлежащего другому пользователю."""
    return mixer.blend(
        Warehouse,
        user=another_user,
        storage_type=StorageTypeChoices.PRODUCT,
        updated_by=another_user,
    )


@pytest.fixture
def file_attachment(mixer, warehouse):
    """Фикстура для создания вложения."""
    test_file_content = b'file_content'
    test_file = SimpleUploadedFile('test_file.txt', test_file_content, content_type='text/plain')
    return FileAttachment.objects.create(
        content_type=ContentType.objects.get_for_model(Warehouse),
        object_id=warehouse.id,
        file=test_file,
    )


@pytest.fixture
def unit_group():
    return UnitGroup.objects.create()


@pytest.fixture
def unit_group_another():
    return UnitGroup.objects.create()


@pytest.fixture
def unit(unit_group):
    unit = Unit.objects.create(
        group=unit_group,
        coefficient=Decimal('1.0'),
    )
    UnitTranslation.objects.create(unit=unit, language_code='ru', title='Метры', short_title='м')
    return unit


@pytest.fixture
def unit_same_group(unit_group):
    unit = Unit.objects.create(
        group=unit_group,
        coefficient=Decimal('0.01'),
    )
    UnitTranslation.objects.create(unit=unit, language_code='ru', title='Сантиметры', short_title='см')
    return unit


@pytest.fixture
def unit_another(unit_group_another):
    unit = Unit.objects.create(
        group=unit_group_another,
        coefficient=Decimal('1.0'),
    )
    UnitTranslation.objects.create(unit=unit, language_code='ru', title='Килограммы', short_title='кг')
    return unit


@pytest.fixture
def material(mixer, warehouse_material, unit, category_material):
    material = mixer.blend(
        Material,
        warehouse=warehouse_material,
        unit=unit,
        price=Decimal('100.50'),
        remaining=Decimal('10.0'),
        min_remaining=Decimal('2.0'),
    )
    material.categories.add(category_material)
    return material


@pytest.fixture
def material_another_user(mixer, warehouse_another_user, unit, category_material):
    warehouse_another_user = mixer.blend(
        Material,
        warehouse=warehouse_another_user,
        unit=unit,
        price=Decimal('100.50'),
        remaining=Decimal('10.0'),
        min_remaining=Decimal('2.0'),
    )
    warehouse_another_user.categories.add(category_material)
    return warehouse_another_user


@pytest.fixture
def resource(mixer, auth_user, unit, category_resource):
    resource = mixer.blend(
        Resource,
        user=auth_user,
        unit=unit,
        is_depreciation=False,
        price=Decimal('1000.00'),
        initial_price=None,
        service_life=None,
        categories=[],
    )
    resource.categories.add(category_resource)
    return resource


@pytest.fixture
def resource_another_user(mixer, another_user, unit, category_resource):
    resource_another_user = mixer.blend(
        Resource,
        user=another_user,
        unit=unit,
        is_depreciation=False,
        price=Decimal('1000.00'),
        initial_price=None,
        service_life=None,
        categories=[],
    )
    resource_another_user.categories.add(category_resource)
    return resource_another_user


@pytest.fixture
def material_data(unit, category_material):
    return {
        'unit': unit.id,
        'title': 'Test Material',
        'sku': 'TEST123',
        'notes': 'Test notes',
        'price': '150.75',
        'remaining': '15.0',
        'min_remaining': '5.0',
        'categories': [category_material.id],
    }


@pytest.fixture
def resource_data(unit, category_resource):
    return {
        'unit': unit.id,
        'title': 'Test Resource',
        'notes': 'Test notes',
        'is_depreciation': False,
        'price': '1500.75',
        'categories': [category_resource.id],
    }


@pytest.fixture
def depreciation_resource_data(unit, category_resource):
    test_file_content = b'file_content'
    test_file = SimpleUploadedFile('test_file.txt', test_file_content, content_type='text/plain')
    return {
        'unit': unit.id,
        'title': 'Depreciation Resource',
        'notes': 'Depreciation notes',
        'is_depreciation': True,
        'initial_price': '2000.00',
        'service_life': '5',
        'categories': [category_resource.id],
        'attachments': [test_file],
    }


@pytest.fixture
def product(mixer, warehouse, unit, category_product):
    product = mixer.blend(
        Product,
        warehouse=warehouse,
        unit=unit,
    )
    product.categories.add(category_product)
    return product


@pytest.fixture
def product_another_user(mixer, warehouse_another_user, unit, category_product):
    product_another_user = mixer.blend(
        Product,
        warehouse=warehouse_another_user,
        unit=unit,
    )
    product_another_user.categories.add(category_product)
    return product_another_user


@pytest.fixture
def product_data(unit, category_product, component_data):
    return {
        'unit': unit.id,
        'title': 'Test Product',
        'sku': 'TEST123',
        'notes': 'Test notes',
        'price': '1500.75',
        'remaining': '150.0',
        'min_remaining': '15.0',
        'categories': [category_product.id],
        'components': [component_data],
    }


@pytest.fixture
def component(mixer, product, material, unit):
    return mixer.blend(
        ProductComponent,
        product=product,
        content_type=ContentType.objects.get_for_model(Material),
        object_id=material.id,
        unit=unit,
        quantity=Decimal('10.0'),
    )


@pytest.fixture
def component_another_user(mixer, product_another_user, material_another_user, unit):
    return mixer.blend(
        ProductComponent,
        product=product_another_user,
        content_type=ContentType.objects.get_for_model(Material),
        object_id=material_another_user.id,
        unit=unit,
        quantity=Decimal('10.0'),
    )


@pytest.fixture
def component_data(material, unit):
    return {
        'content_type': ProductComponentChoices.MATERIAL,
        'object_id': material.id,
        'quantity': '5.0',
        'unit': unit.id,
    }
