import dataclasses
from decimal import Decimal

from apps.unit.models import Unit


@dataclasses.dataclass
class AttachmentsDTO:
    filename: str | None = None
    file: bytes | None = None


@dataclasses.dataclass
class ProductComponentDTO:
    content_type: str
    object_id: int
    quantity: Decimal
    unit: Unit
    user_id: int
    id: int | None = None
