import pytest
from rest_framework import status

from apps.warehouse.choices import CategoryTypeChoices
from apps.warehouse.models import Category


@pytest.mark.django_db
class TestCategoryCRUD:
    BASE_URL = '/api/v1/warehouse/category/'

    def test_get_category_list(self, auth_api_test_client, auth_user, categories_list):
        """Тест получения списка категорий."""

        response = auth_api_test_client.get(self.BASE_URL)
        assert len(response) == 3
        assert all(cat['user'] == auth_user.id for cat in response)

    def test_get_category_detail(self, auth_api_test_client, category_product):
        """Тест получения одной категории."""

        response = auth_api_test_client.get(f'{self.BASE_URL}{category_product.id}/')
        assert response['id'] == category_product.id
        assert response['title'] == category_product.title
        assert 'category_type' in response
        assert 'value' in response['category_type']
        assert 'label' in response['category_type']

    def test_create_category(self, auth_api_test_client):
        """Тест создания категории."""
        category_data = {'title': 'Test Category', 'category_type': CategoryTypeChoices.choices[0][0]}

        response = auth_api_test_client.post(self.BASE_URL, data=category_data)

        assert Category.objects.filter(id=response['id']).exists()
        created_category = Category.objects.get(id=response['id'])
        assert created_category.title == category_data['title']
        assert created_category.category_type == category_data['category_type']
        assert created_category.user == auth_api_test_client.user

    def test_update_category(self, auth_api_test_client, category_product):
        """Тест обновления категории."""
        update_data = {
            'title': 'Updated Title',
        }

        response = auth_api_test_client.put(f'{self.BASE_URL}{category_product.id}/', data=update_data)

        category = Category.objects.get(id=category_product.id)
        assert category.title == update_data['title']
        assert response['title'] == update_data['title']

    def test_delete_category(self, auth_api_test_client, category_product):
        """Тест удаления категории."""

        auth_api_test_client.delete(f'{self.BASE_URL}{category_product.id}/')

        assert not Category.objects.filter(id=category_product.id).exists()

    def test_other_user_cant_access_categories(self, auth_api_test_client, category_another_user):
        """Тест на то что пользователь не может получить доступ к категориям другого пользователя."""

        auth_api_test_client.get(
            f'{self.BASE_URL}{category_another_user.id}/',
            expected_status=status.HTTP_404_NOT_FOUND,
        )

    def est_unauthenticated_access(self, api_test_client):
        """Не авторизованный пользователь."""
        api_test_client.get(self.BASE_URL, expected_status=status.HTTP_401_UNAUTHORIZED)
