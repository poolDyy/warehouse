import os

import pytest
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from apps.warehouse.choices import ContentTypeChoices
from apps.warehouse.models import FileAttachment, Warehouse


@pytest.mark.django_db
class TestFileAttachmentCRUD:
    BASE_URL = '/api/v1/warehouse/file-attachment/'

    def test_create_file_attachment(self, auth_api_test_client, warehouse):
        """Тест создания вложения."""
        test_file = SimpleUploadedFile('test_file.txt', b'file_content', content_type='text/plain')
        data = {
            'content_type': ContentTypeChoices.WAREHOUSE,
            'object_id': warehouse.id,
            'file': test_file,
        }

        response = auth_api_test_client.post(
            self.BASE_URL,
            data=data,
            format='multipart',
        )

        attachment = FileAttachment.objects.get(id=response['id'])
        assert attachment.content_type == ContentType.objects.get_for_model(Warehouse)
        assert attachment.object_id == warehouse.id
        assert os.path.basename(attachment.file.name) == 'test_file.txt'

    def test_retrieve_file_attachment(self, auth_api_test_client, warehouse):
        """Тест получения скачиваемого файла."""

        test_file_content = b'file_content'
        test_file = SimpleUploadedFile('test_file.txt', test_file_content, content_type='text/plain')
        file_attachment = FileAttachment.objects.create(
            content_type=ContentType.objects.get_for_model(Warehouse),
            object_id=warehouse.id,
            file=test_file,
        )

        response = auth_api_test_client.api_client.get(f'{self.BASE_URL}{file_attachment.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/plain'
        assert response['Content-Disposition'] == 'attachment; filename="test_file.txt"'
        assert int(response['Content-Length']) == len(test_file_content)
        assert b''.join(response.streaming_content) == test_file_content

    def test_delete_file_attachment(self, auth_api_test_client, warehouse, file_attachment):
        """Тест удаления вложения."""

        auth_api_test_client.delete(f'{self.BASE_URL}{file_attachment.id}/')
        assert not FileAttachment.objects.filter(id=file_attachment.id).exists()

    def test_create_file_attachment_invalid_content_type(self, auth_api_test_client, warehouse):
        """Тест ошибки при некорректном content_type."""
        test_file = SimpleUploadedFile('test_file.txt', b'file_content', content_type='text/plain')
        data = {
            'content_type': 'invalid_model',
            'object_id': warehouse.id,
            'file': test_file,
        }

        response = auth_api_test_client.post(
            self.BASE_URL,
            data=data,
            format='multipart',
            expected_status=status.HTTP_400_BAD_REQUEST,
        )
        assert 'content_type' in response

    def test_retrieve_missing_file(self, auth_api_test_client, warehouse):
        """Тест ошибки при отсутствии файла на диске."""
        test_file = SimpleUploadedFile('test_file.txt', b'file_content', content_type='text/plain')
        attachment = FileAttachment.objects.create(
            content_type=ContentType.objects.get_for_model(Warehouse), object_id=warehouse.id, file=test_file
        )

        os.remove(os.path.join(settings.MEDIA_ROOT, attachment.file.name))
        auth_api_test_client.get(f'{self.BASE_URL}{attachment.id}/', expected_status=status.HTTP_400_BAD_REQUEST)

    def test_retrieve_file_attachment_of_another_user(self, auth_api_test_client, warehouse_another_user):
        """Тест ошибки при попытке получить файл к которому нет прав."""

        test_file_content = b'file_content'
        test_file = SimpleUploadedFile('test_file.txt', test_file_content, content_type='text/plain')
        file_attachment = FileAttachment.objects.create(
            content_type=ContentType.objects.get_for_model(Warehouse),
            object_id=warehouse_another_user.id,
            file=test_file,
        )

        auth_api_test_client.get(
            f'{self.BASE_URL}{file_attachment.id}/',
            expected_status=status.HTTP_403_FORBIDDEN,
        )
