import logging
from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

__all__ = [
    'ApiTestClient',
    'ApiTestClientAuth',
]


User = get_user_model()

logger = logging.getLogger(__name__)


class BaseApiTestClient(ABC, APIClient):
    @property
    @abstractmethod
    def api_client(self) -> APIClient:
        pass

    def get(
        self,
        *args,
        format='json',
        expected_status: int = status.HTTP_200_OK,
        **kwargs,
    ):
        response = self.api_client.get(*args, format=format, **kwargs)
        assert response.status_code == expected_status
        return response.json()

    def post(
        self,
        *args,
        format='json',
        expected_status: int = status.HTTP_201_CREATED,
        **kwargs,
    ):
        response = self.api_client.post(*args, format=format, **kwargs)
        assert response.status_code == expected_status
        return response.json()

    def put(
        self,
        *args,
        format='json',
        expected_status: int = status.HTTP_200_OK,
        **kwargs,
    ):
        response = self.api_client.put(*args, format=format, **kwargs)
        print(response.json())

        assert response.status_code == expected_status
        return response.json()

    def patch(
        self,
        *args,
        format='json',
        expected_status: int = status.HTTP_200_OK,
        **kwargs,
    ):
        response = self.api_client.patch(*args, format=format, **kwargs)
        assert response.status_code == expected_status
        return response.json()

    def delete(
        self,
        *args,
        format='json',
        expected_status: int = status.HTTP_204_NO_CONTENT,
        **kwargs,
    ):
        response = self.api_client.delete(*args, format=format, **kwargs)
        assert response.status_code == expected_status
        return response


class ApiTestClient(BaseApiTestClient):
    @property
    def api_client(self) -> APIClient:
        return APIClient()


class ApiTestClientAuth(BaseApiTestClient):
    def __init__(self, *args, user: User, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = user

    @property
    def api_client(self) -> APIClient:
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        return client
