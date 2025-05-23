import pytest
from rest_framework import status

from apps.warehouse.choices import StorageTypeChoices
from apps.warehouse.models import Warehouse


@pytest.mark.django_db
class TestWarehouseCRUD:
    BASE_URL = '/api/v1/warehouse/'

    def test_get_warehouse_list(self, auth_api_test_client, warehouse):
        """Тест получения списка складов."""
        response = auth_api_test_client.get(self.BASE_URL)
        assert isinstance(response, list)
        assert any(w['id'] == warehouse.id for w in response)
        assert response[0]['title'] == warehouse.title
        assert response[0]['storage_type']['value'] == warehouse.storage_type

    def test_get_warehouse_detail(self, auth_api_test_client, warehouse, category_product):
        """Тест получения деталей склада."""
        warehouse.categories.add(category_product)
        response = auth_api_test_client.get(f'{self.BASE_URL}{warehouse.id}/')
        assert response['id'] == warehouse.id
        assert response['title'] == warehouse.title
        assert response['storage_type']['value'] == warehouse.storage_type
        assert len(response['categories']) == 1
        assert response['categories'][0]['id'] == category_product.id

    def test_create_warehouse(self, auth_api_test_client, category_product):
        """Тест создания склада."""
        data = {
            'title': 'Новый склад',
            'storage_type': StorageTypeChoices.PRODUCT,
            'categories': [category_product.id],
        }

        response = auth_api_test_client.post(
            self.BASE_URL,
            data=data,
        )

        created_warehouse = Warehouse.objects.get(id=response['id'])
        assert created_warehouse.title == 'Новый склад'
        assert created_warehouse.storage_type == StorageTypeChoices.PRODUCT
        assert created_warehouse.categories.count() == 1
        assert created_warehouse.categories.first().id == category_product.id

    def test_create_warehouse_invalid_storage_type(self, auth_api_test_client, category_material):
        """Тест создания склада с категориями не подходящими под тип склада."""
        data = {
            'title': 'Новый склад',
            'storage_type': StorageTypeChoices.PRODUCT,
            'categories': [category_material.id],
        }

        response = auth_api_test_client.post(self.BASE_URL, data=data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'categories' in response
        assert 'Категории не подходят под тип склада:' in str(response['categories'])

    def test_update_warehouse(self, auth_api_test_client, warehouse, category_resource):
        """Тест обновления склада."""

        data = {
            'title': 'Обновлённый склад',
            'storage_type': StorageTypeChoices.PRODUCT,
            'categories': [category_resource.id],
        }

        auth_api_test_client.put(f'{self.BASE_URL}{warehouse.id}/', data=data)

        updated_warehouse = Warehouse.objects.get(id=warehouse.id)
        assert updated_warehouse.title == 'Обновлённый склад'
        assert updated_warehouse.categories.count() == 1
        assert updated_warehouse.categories.first().id == category_resource.id

    def test_delete_warehouse(self, auth_api_test_client, warehouse):
        """Тест удаления склада."""
        auth_api_test_client.delete(f'{self.BASE_URL}{warehouse.id}/')

        assert not Warehouse.objects.filter(id=warehouse.id).exists()

    def test_unauthenticated_access(self, api_test_client):
        """Тест доступа без аутентификации."""
        api_test_client.get(self.BASE_URL, expected_status=status.HTTP_401_UNAUTHORIZED)

    def test_has_warehouse_of_another_user_access(self, auth_api_test_client, warehouse_another_user):
        """Тест доступа без аутентификации."""
        auth_api_test_client.get(
            f'{self.BASE_URL}{warehouse_another_user.id}/',
            expected_status=status.HTTP_404_NOT_FOUND,
        )
