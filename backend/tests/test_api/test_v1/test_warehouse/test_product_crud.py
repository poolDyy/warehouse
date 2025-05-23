from decimal import Decimal

import pytest
from django.contrib.contenttypes.models import ContentType
from rest_framework import status

from apps.warehouse.choices import ProductComponentChoices
from apps.warehouse.models import (
    Material,
    Product,
    ProductComponent,
)


@pytest.mark.django_db
class TestProductCRUD:
    BASE_URL = '/api/v1/warehouse/{warehouse_id}/products/'

    def test_get_product_list(self, auth_api_test_client, warehouse, product):
        """Успешное получение списка продуктов."""
        url = self.BASE_URL.format(warehouse_id=warehouse.id)
        response = auth_api_test_client.get(url)

        data = response['results']

        assert len(data) == 1
        assert data[0]['id'] == product.id

    def test_get_product_detail(self, auth_api_test_client, warehouse, product):
        """Успешное получение деталей продукта."""
        url = f'{self.BASE_URL.format(warehouse_id=warehouse.id)}{product.id}/'
        response = auth_api_test_client.get(url)

        assert response['id'] == product.id
        assert response['title'] == product.title

    def test_create_product(self, auth_api_test_client, warehouse, unit, product_data):
        """Успешное создание продукта."""
        url = self.BASE_URL.format(warehouse_id=warehouse.id)
        response = auth_api_test_client.post(url, data=product_data)

        new_product = Product.objects.get(id=response['id'])
        assert new_product.title == product_data['title']
        assert new_product.components.count() == 1

    def test_update_product(self, auth_api_test_client, warehouse, product, product_data):
        """Успешное обновление продукта."""
        url = f'{self.BASE_URL.format(warehouse_id=warehouse.id)}{product.id}/'
        product_data['title'] = 'Updated Title'
        auth_api_test_client.put(url, data=product_data)

        product.refresh_from_db()

        assert product.title == 'Updated Title'

    def test_update_product_with_components(
        self,
        mixer,
        auth_api_test_client,
        warehouse,
        product,
        product_data,
        material,
        unit,
    ):
        """Успешное обновление продукта с компонентами."""
        component_new = mixer.blend(
            ProductComponent,
            product=product,
            content_type=ContentType.objects.get_for_model(Material),
            object_id=material.id,
            unit=unit,
            quantity=Decimal('10.0'),
        )

        url = f'{self.BASE_URL.format(warehouse_id=warehouse.id)}{product.id}/'
        product_data['components'] = [
            {
                'id': component_new.id,
                'quantity': '15.0',
                'unit': unit.id,
                'content_type': ProductComponentChoices.MATERIAL,
                'object_id': material.id,
            }
        ]
        response = auth_api_test_client.put(url, data=product_data)
        assert 'components' in response
        assert Decimal(response['components'][0]['quantity']) == Decimal('15.0')

    def test_update_product_with_components_already_exists(
        self,
        mixer,
        auth_api_test_client,
        warehouse,
        product,
        product_data,
        material,
        unit,
    ):
        """Обновление продукта с задвоенным компонентом."""
        component_new = mixer.blend(
            ProductComponent,
            product=product,
            content_type=ContentType.objects.get_for_model(Material),
            object_id=material.id,
            unit=unit,
            quantity=Decimal('10.0'),
        )

        url = f'{self.BASE_URL.format(warehouse_id=warehouse.id)}{product.id}/'
        product_data['components'].append(
            {
                'id': component_new.id,
                'quantity': '15.0',
                'unit': unit.id,
                'content_type': ProductComponentChoices.MATERIAL,
                'object_id': material.id,
            }
        )
        response = auth_api_test_client.put(url, data=product_data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'components' in response
        assert response['components']['0']['object_id'] == 'Компонент уже находится в составе продукта'

    def test_delete_product(self, auth_api_test_client, warehouse, product):
        """Успешное удаление продукта."""
        url = f'{self.BASE_URL.format(warehouse_id=warehouse.id)}{product.id}/'
        auth_api_test_client.delete(url)

        assert not Product.objects.filter(id=product.id).exists()

    def test_create_product_invalid_warehouse_type(self, auth_api_test_client, warehouse_material, product_data):
        """Ошибка при создании продукта в складе неправильного типа."""
        url = self.BASE_URL.format(warehouse_id=warehouse_material.id)
        response = auth_api_test_client.post(url, data=product_data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'warehouse' in response

    def test_create_product_invalid_categories(
        self, auth_api_test_client, category_another_user, warehouse, product_data
    ):
        """Ошибка при создании продукта с категориями не из этого склада."""
        product_data['categories'].append(category_another_user.id)
        response = auth_api_test_client.post(
            self.BASE_URL.format(warehouse_id=warehouse.id),
            data=product_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )
        assert 'categories' in response

    def test_create_product_invalid_component(
        self, auth_api_test_client, warehouse, product_data, material_another_user, unit
    ):
        """Ошибка при создании продукта с чужим компонентом."""
        url = self.BASE_URL.format(warehouse_id=warehouse.id)
        product_data['components'] = [
            {
                'content_type': ProductComponentChoices.MATERIAL,
                'object_id': material_another_user.id,
                'quantity': '5.0',
                'unit': unit.id,
            }
        ]
        response = auth_api_test_client.post(url, data=product_data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'components' in response

    def test_unauthenticated_access(self, api_test_client, warehouse):
        """Ошибка доступа без аутентификации."""
        api_test_client.get(
            self.BASE_URL.format(warehouse_id=warehouse.id),
            expected_status=status.HTTP_401_UNAUTHORIZED,
        )

    def test_access_to_other_user_warehouse(self, auth_api_test_client, warehouse_another_user):
        """Ошибка доступа к складу другого пользователя."""
        auth_api_test_client.get(
            self.BASE_URL.format(warehouse_id=warehouse_another_user.id),
            expected_status=status.HTTP_403_FORBIDDEN,
        )
