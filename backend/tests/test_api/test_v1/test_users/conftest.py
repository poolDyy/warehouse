import pytest

from apps.users.models import User


@pytest.fixture
def user(mixer):
    """Создает пользователя."""
    return mixer.blend(User)


@pytest.fixture
def user_data():
    """Тестовые данные для пользователя."""
    return {
        'email': 'test@test.ru',
        'password': 'TestPassword123!',
        'repeat_password': 'TestPassword123!',
    }
