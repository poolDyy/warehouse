import os
import shutil
import tempfile

import pytest
from django.test import override_settings
from mixer.backend.django import mixer as _mixer

from apps.users.models import User

from .common import ApiTestClient, ApiTestClientAuth


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def api_test_client():
    return ApiTestClient()


def create_user(mixer, **kwargs):
    password = kwargs.pop('password', 'testpassword123!')
    user = mixer.blend(User, **kwargs)
    user.set_password(password)
    user.save()
    return user


@pytest.fixture
def auth_user(mixer):
    """Фикстура для создания тестового пользователя."""
    return create_user(mixer, email='test@user.ru', telegram_user=None)


@pytest.fixture
def auth_api_test_client(auth_user):
    """Фикстура для создания авторизованного клиента."""
    return ApiTestClientAuth(
        user=auth_user,
    )


@pytest.fixture(scope='session', autouse=True)
def temporary_media_root():
    # Создаем временную папку для MEDIA_ROOT
    temp_dir = tempfile.mkdtemp()

    # Переопределяем MEDIA_ROOT на время тестов
    with override_settings(MEDIA_ROOT=temp_dir):
        yield  # Выполняем тесты

    # Удаляем временную папку после всех тестов
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
