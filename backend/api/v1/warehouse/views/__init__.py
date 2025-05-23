from .categories import CategoryViewSet
from .file_attachment import FileAttachmentViewSet
from .material import MaterialViewSet
from .product_component import ProductComponentViewSet
from .product import ProductViewSet
from .resource import ResourceViewSet
from .warehouse import WarehouseViewSet

__all__ = [
    'WarehouseViewSet',
    'CategoryViewSet',
    'FileAttachmentViewSet',
    'MaterialViewSet',
    'ResourceViewSet',
    'ProductComponentViewSet',
    'ProductViewSet',
]
