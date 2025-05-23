import dataclasses

from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile

from apps.warehouse.choices import ContentTypeChoices
from apps.warehouse.models import FileAttachment, Material, Product, Resource, Warehouse


@dataclasses.dataclass
class FileAttachmentCreateService:
    filename: str
    file: bytes

    @property
    def content_type_map(self) -> dict:
        return {
            ContentTypeChoices.PRODUCT: ContentType.objects.get_for_model(Product),
            ContentTypeChoices.MATERIAL: ContentType.objects.get_for_model(Material),
            ContentTypeChoices.RESOURCE: ContentType.objects.get_for_model(Resource),
            ContentTypeChoices.WAREHOUSE: ContentType.objects.get_for_model(Warehouse),
        }

    def create(
        self,
        content_type_str: str,
        object_id: int,
    ) -> FileAttachment:
        content_type = self.content_type_map.get(content_type_str)
        if content_type is None:
            raise Exception(f'Unknown content type "{content_type_str}"')
        content_file = ContentFile(self.file, name=self.filename)
        attachment = FileAttachment(content_type=content_type, object_id=object_id, file=content_file)
        attachment.save()
        return attachment
