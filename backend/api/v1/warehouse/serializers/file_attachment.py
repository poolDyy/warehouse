from rest_framework import serializers

from apps.warehouse.choices import ContentTypeChoices
from apps.warehouse.models import FileAttachment


class FileAttachmentSerializer(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(
        choices=ContentTypeChoices.choices,
        write_only=True,
    )
    object_id = serializers.IntegerField(
        min_value=1,
        write_only=True,
    )

    class Meta:
        model = FileAttachment
        fields = [
            'id',
            'content_type',
            'object_id',
            'file',
        ]
