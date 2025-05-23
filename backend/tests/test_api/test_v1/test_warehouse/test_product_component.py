from decimal import Decimal

import pytest
from rest_framework import status

from apps.warehouse.choices import ProductComponentChoices
from apps.warehouse.models import ProductComponent


@pytest.mark.django_db
class TestProductComponentCRUD:
    BASE_URL = '/api/v1/warehouse/products/{product_id}/components/'

    def test_get_component_list(self, auth_api_test_client, product, component):
        """Успешное получение списка компонентов."""
        url = self.BASE_URL.format(product_id=product.id)
        response = auth_api_test_client.get(url)

        assert len(response) == 1
        assert response[0]['id'] == component.id

    def test_get_component_detail(self, auth_api_test_client, product, component):
        """Успешное получение деталей компонента."""
        url = f'{self.BASE_URL.format(product_id=product.id)}{component.id}/'
        response = auth_api_test_client.get(url)

        assert response['id'] == component.id
        assert Decimal(response['quantity']) == component.quantity

    def test_create_material_component(self, auth_api_test_client, product, material, unit, component_data):
        """Успешное создание компонента из материала."""
        url = self.BASE_URL.format(product_id=product.id)
        response = auth_api_test_client.post(url, data=component_data)

        assert ProductComponent.objects.filter(id=response['id']).exists()

    def test_create_resource_component(self, auth_api_test_client, product, resource, unit):
        """Успешное создание компонента из ресурса."""
        url = self.BASE_URL.format(product_id=product.id)
        data = {
            'content_type': ProductComponentChoices.RESOURCE,
            'object_id': resource.id,
            'quantity': '3.0',
            'unit': unit.id,
        }
        auth_api_test_client.post(url, data=data)

    def test_update_component(self, auth_api_test_client, product, component, unit_same_group):
        """Успешное обновление компонента."""
        url = f'{self.BASE_URL.format(product_id=product.id)}{component.id}/'
        data = {
            'quantity': '15.0',
            'content_type': ProductComponentChoices.MATERIAL,
            'object_id': component.object_id,
            'unit': unit_same_group.id,
        }
        auth_api_test_client.put(url, data=data)

        component.refresh_from_db()
        assert component.quantity == Decimal('15.0')

    def test_delete_component(self, auth_api_test_client, product, component):
        """Успешное удаление компонента."""
        url = f'{self.BASE_URL.format(product_id=product.id)}{component.id}/'
        auth_api_test_client.delete(url)

        assert not ProductComponent.objects.filter(id=component.id).exists()

    def test_create_component_invalid_quantity(self, auth_api_test_client, product, material, unit):
        """Ошибка при невалидном количестве (<= 0)."""
        url = self.BASE_URL.format(product_id=product.id)
        data = {
            'content_type': ProductComponentChoices.MATERIAL,
            'object_id': material.id,
            'quantity': '-1',
            'unit': unit.id,
        }
        response = auth_api_test_client.post(url, data=data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'quantity' in response

    def test_create_component_unauthorized_material(self, auth_api_test_client, product, material_another_user, unit):
        """Ошибка при использовании чужого материала."""
        url = self.BASE_URL.format(product_id=product.id)
        data = {
            'content_type': ProductComponentChoices.MATERIAL,
            'object_id': material_another_user.id,
            'quantity': '5.0',
            'unit': unit.id,
        }
        response = auth_api_test_client.post(url, data=data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'content_type' in response

    def test_create_component_invalid_unit(self, auth_api_test_client, product, material, unit_another):
        """Ошибка при несоответствующей единице измерения."""
        url = self.BASE_URL.format(product_id=product.id)

        data = {
            'content_type': ProductComponentChoices.MATERIAL,
            'object_id': material.id,
            'quantity': '5.0',
            'unit': unit_another.id,
        }
        response = auth_api_test_client.post(url, data=data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'unit' in response

    def test_create_component_invalid_content_type(self, auth_api_test_client, product, material, unit):
        """Ошибка при невалидном типе контента."""
        url = self.BASE_URL.format(product_id=product.id)
        data = {'content_type': 'invalid_type', 'object_id': material.id, 'quantity': '5.0', 'unit': unit.id}
        response = auth_api_test_client.post(url, data=data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'content_type' in response

    def test_create_component_nonexistent_object(self, auth_api_test_client, product, unit):
        """Ошибка при несуществующем объекте компонента."""
        url = self.BASE_URL.format(product_id=product.id)
        data = {
            'content_type': ProductComponentChoices.MATERIAL,
            'object_id': 9999,  # Несуществующий ID
            'quantity': '5.0',
            'unit': unit.id,
        }
        response = auth_api_test_client.post(url, data=data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'object_id' in response

    def test_unauthenticated_access(self, api_test_client, product):
        """Ошибка доступа без аутентификации."""
        url = self.BASE_URL.format(product_id=product.id)
        api_test_client.get(url, expected_status=status.HTTP_401_UNAUTHORIZED)

    def test_access_to_other_user_product(self, auth_api_test_client, product_another_user):
        """Ошибка доступа к продукту другого пользователя."""
        url = self.BASE_URL.format(product_id=product_another_user.id)
        response = auth_api_test_client.get(url, expected_status=status.HTTP_403_FORBIDDEN)
        assert 'detail' in response

    def test_update_other_user_component(
        self, auth_api_test_client, component_another_user, product_another_user, unit
    ):
        """Ошибка при обновлении компонента чужого продукта."""

        url = f'{self.BASE_URL.format(product_id=product_another_user.id)}{component_another_user.id}/'
        data = {'quantity': '15.0', 'unit': unit.id}
        auth_api_test_client.put(url, data=data, expected_status=status.HTTP_403_FORBIDDEN)
