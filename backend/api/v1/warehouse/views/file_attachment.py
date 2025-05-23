import mimetypes
import os
from typing import Any

from django.db.models import QuerySet
from django.http import FileResponse
from rest_framework import serializers, status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.common.permissions import HasUserObjPerms
from api.common.views import BaseGenericViewSet
from api.v1.warehouse.serializers import FileAttachmentSerializer
from apps.warehouse.models import FileAttachment
from apps.warehouse.services.file_attachment import FileAttachmentCreateService


class FileAttachmentViewSet(
    DestroyModelMixin,
    BaseGenericViewSet,
    CreateModelMixin,
):
    serializer_class = FileAttachmentSerializer

    permission_classes = [IsAuthenticated, HasUserObjPerms]

    def get_queryset(self) -> QuerySet:
        return FileAttachment.objects.all()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = self.get_serializer(instance=instance).data
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer: FileAttachmentSerializer) -> FileAttachment:
        file_attachment = serializer.validated_data['file']
        service = FileAttachmentCreateService(
            filename=file_attachment.name,
            file=file_attachment.read(),
        )
        return service.create(
            content_type_str=serializer.validated_data['content_type'],
            object_id=serializer.validated_data['object_id'],
        )

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> FileResponse:
        instance = self.get_object()
        file_path = instance.file.path
        if not os.path.exists(file_path):
            raise serializers.ValidationError({'id': 'Файл не найден'})
        file_handle = open(file_path, 'rb')

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        response = FileResponse(file_handle, content_type=mime_type)
        file_name = os.path.basename(file_path)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        response['Content-Length'] = instance.file.size
        return response
