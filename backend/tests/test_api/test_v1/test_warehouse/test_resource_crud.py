from decimal import Decimal

import pytest
from rest_framework import status

from apps.warehouse.models import Resource


@pytest.mark.django_db
class TestResourceCRUD:
    BASE_URL = '/api/v1/warehouse/resources/'

    def test_get_resource_list(self, auth_api_test_client, resource):
        """Тест получения списка ресурсов."""
        response = auth_api_test_client.get(self.BASE_URL)

        assert len(response) == 1
        assert response[0]['id'] == resource.id
        assert response[0]['title'] == resource.title

    def test_get_resource_detail(self, auth_api_test_client, resource):
        """Тест получения одного ресурса."""
        url = f'{self.BASE_URL}{resource.id}/'
        response = auth_api_test_client.get(url)

        assert response['id'] == resource.id
        assert response['title'] == resource.title
        assert response['user'] == resource.user.id
        assert len(response['categories']) == resource.categories.count()

    def test_create_resource(self, auth_api_test_client, resource_data):
        """Тест создания ресурса."""
        response = auth_api_test_client.post(self.BASE_URL, data=resource_data)

        assert Resource.objects.filter(id=response['id']).exists()
        new_resource = Resource.objects.get(id=response['id'])
        assert new_resource.title == resource_data['title']
        assert new_resource.is_depreciation == resource_data['is_depreciation']
        assert new_resource.price == Decimal(resource_data['price'])
        assert new_resource.categories.count() == len(resource_data['categories'])

    def test_create_depreciation_resource(self, auth_api_test_client, depreciation_resource_data):
        """Тест создания ресурса с амортизацией."""
        response = auth_api_test_client.post(self.BASE_URL, data=depreciation_resource_data)
        new_resource = Resource.objects.get(id=response['id'])
        assert new_resource.is_depreciation
        assert new_resource.initial_price == Decimal(depreciation_resource_data['initial_price'])
        assert new_resource.service_life == Decimal(depreciation_resource_data['service_life'])
        assert new_resource.price is None

    def test_update_resource(self, auth_api_test_client, resource, resource_data):
        """Тест обновления ресурса."""
        url = f'{self.BASE_URL}{resource.id}/'
        resource_data['title'] = 'Updated Title'

        response = auth_api_test_client.put(url, data=resource_data)
        updated_resource = Resource.objects.get(id=response['id'])
        assert updated_resource.title == 'Updated Title'

    def test_delete_resource(self, auth_api_test_client, resource):
        """Тест удаления ресурса."""
        url = f'{self.BASE_URL}{resource.id}/'
        auth_api_test_client.delete(url)

        assert not Resource.objects.filter(id=resource.id).exists()

    def test_create_resource_invalid_categories(self, auth_api_test_client, resource_data, category_another_user):
        """Тест создания ресурса с категориями не принадлежащими пользователю."""
        resource_data['categories'].append(category_another_user.id)

        response = auth_api_test_client.post(
            self.BASE_URL,
            data=resource_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )
        assert 'categories' in response

    def test_create_resource_wrong_category_type(self, auth_api_test_client, resource_data, category_material):
        """Тест создания ресурса с категориями неправильного типа."""
        resource_data['categories'] = [category_material.id]

        response = auth_api_test_client.post(
            self.BASE_URL,
            data=resource_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )
        assert 'categories' in response

    def test_create_depreciation_resource_missing_fields(self, auth_api_test_client, depreciation_resource_data):
        """Тест создания ресурса с амортизацией без обязательных полей."""
        depreciation_resource_data.pop('initial_price')

        response = auth_api_test_client.post(
            self.BASE_URL,
            data=depreciation_resource_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )
        assert 'is_depreciation' in response

    def test_create_non_depreciation_resource_missing_price(self, auth_api_test_client, resource_data):
        """Тест создания ресурса без амортизации без цены."""
        resource_data.pop('price')

        response = auth_api_test_client.post(
            self.BASE_URL,
            data=resource_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )
        assert 'price' in response

    def test_unauthenticated_access(self, api_test_client):
        """Тест доступа без аутентификации."""
        api_test_client.get(self.BASE_URL, expected_status=status.HTTP_401_UNAUTHORIZED)

    def test_has_warehouse_of_another_user_access(self, auth_api_test_client, resource_another_user):
        """Тест доступа без аутентификации."""
        auth_api_test_client.get(
            f'{self.BASE_URL}{resource_another_user.id}/',
            expected_status=status.HTTP_404_NOT_FOUND,
        )
