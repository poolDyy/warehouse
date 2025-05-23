from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


def get_attachment_upload_path(instance: 'FileAttachment', filename: str) -> str:
    content_type = instance.content_type
    objects_id = instance.object_id

    app_label = content_type.app_label
    model_name = content_type.model

    current_date = datetime.now()
    year = current_date.strftime('%Y')
    month = current_date.strftime('%m')
    day = current_date.strftime('%d')

    path = f'attachments/{app_label}/{model_name}/{objects_id}/{year}/{month}/{day}/{filename}'

    return path


class FileAttachment(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ['product', 'material', 'resource', 'warehouse']},
    )
    object_id = models.PositiveIntegerField()
    attached_to = GenericForeignKey(
        'content_type',
        'object_id',
    )
    file = models.FileField(
        upload_to=get_attachment_upload_path,
        verbose_name='Файл',
    )

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self) -> str:
        return f'{self.file.name}'

    def user_obj_permission(self, user_id: int) -> bool:
        """Проверяет, имеет ли пользователь право на операцию над моделью."""
        model_instance = self.content_type.model_class().objects.filter(pk=self.object_id).first()
        if hasattr(model_instance, 'user_obj_permission'):
            return model_instance.user_obj_permission(user_id)
        return False
