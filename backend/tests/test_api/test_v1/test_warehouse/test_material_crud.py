import pytest
from rest_framework import status

from apps.warehouse.models import Category, Material


@pytest.mark.django_db
class TestMaterialCRUD:
    BASE_URL = '/api/v1/warehouse/{warehouse_id}/materials/'

    def test_get_material_list(self, auth_api_test_client, warehouse_material, material):
        """Тест получения списка материалов."""
        url = self.BASE_URL.format(warehouse_id=warehouse_material.id)
        response = auth_api_test_client.get(url)

        data = response['results']

        assert len(data) == 1
        assert data[0]['id'] == material.id
        assert data[0]['title'] == material.title

    def test_get_material_detail(self, auth_api_test_client, warehouse_material, material):
        """Тест получения одного материала."""
        url = f'{self.BASE_URL.format(warehouse_id=warehouse_material.id)}{material.id}/'
        response = auth_api_test_client.get(url)

        assert response['id'] == material.id
        assert response['title'] == material.title
        assert response['warehouse']['id'] == warehouse_material.id
        assert len(response['categories']) == material.categories.count()
        assert response['unit']['title'] == material.unit.translations.filter(language_code='ru').first().title

    def test_create_material(self, auth_api_test_client, warehouse_material, unit, material_data):
        """Тест создания материала."""
        url = self.BASE_URL.format(warehouse_id=warehouse_material.id)
        response = auth_api_test_client.post(url, data=material_data)

        assert Material.objects.filter(id=response['id']).exists()
        new_material = Material.objects.get(id=response['id'])
        assert new_material.title == material_data['title']
        assert new_material.warehouse == warehouse_material
        assert new_material.categories.count() == len(material_data['categories'])

    def test_update_material(self, auth_api_test_client, warehouse_material, material, material_data):
        """Тест обновления материала."""
        url = f'{self.BASE_URL.format(warehouse_id=warehouse_material.id)}{material.id}/'
        material_data['title'] = 'Updated Title'

        auth_api_test_client.put(url, data=material_data)

        material.refresh_from_db()
        assert material.title == material_data['title']

    def test_delete_material(self, auth_api_test_client, warehouse_material, material):
        """Тест удаления материала."""
        url = f'{self.BASE_URL.format(warehouse_id=warehouse_material.id)}{material.id}/'
        auth_api_test_client.delete(url)
        assert not Material.objects.filter(id=material.id).exists()

    def test_create_material_invalid_warehouse_type(self, auth_api_test_client, warehouse, material_data):
        """Тест создания материала в складе неправильного типа."""
        url = self.BASE_URL.format(warehouse_id=warehouse.id)

        response = auth_api_test_client.post(url, data=material_data, expected_status=status.HTTP_400_BAD_REQUEST)
        assert 'warehouse' in response
        assert 'Склад не предназначен для материалов' in response['warehouse']

    def test_create_material_invalid_categories(self, mixer, auth_api_test_client, warehouse_material, material_data):
        """Тест создания материала с категориями не из этого склада."""
        invalid_category = mixer.blend(Category)  # Категория из другого склада
        material_data['categories'].append(invalid_category.id)

        url = self.BASE_URL.format(warehouse_id=warehouse_material.id)
        response = auth_api_test_client.post(url, data=material_data, expected_status=status.HTTP_400_BAD_REQUEST)

        assert 'categories' in response
        assert 'Исключите категории не принадлежащие складу' in response['categories']

    def test_unauthenticated_access(self, api_test_client, warehouse_material):
        """Тест доступа без аутентификации."""
        api_test_client.get(
            self.BASE_URL.format(warehouse_id=warehouse_material.id),
            expected_status=status.HTTP_401_UNAUTHORIZED,
        )

    def test_has_warehouse_of_another_user_access(
        self,
        auth_api_test_client,
        material_another_user,
    ):
        """Тест доступа без аутентификации."""
        auth_api_test_client.get(
            f'{self.BASE_URL.format(warehouse_id=material_another_user.warehouse_id)}{material_another_user.id}/',
            expected_status=status.HTTP_403_FORBIDDEN,
        )
