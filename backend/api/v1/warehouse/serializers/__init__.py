from .categories import CategoryCreateSerializer, CategoryResponseSerializer
from .material import MaterialCreateSerializer, MaterialResponseSerializer, MaterialUpdateSerializer
from .product import ProductCreateSerializer, ProductUpdateSerializer, ProductDetailSerializer, ProductListSerializer
from .product_component import (
    ProductComponentCreateSerializer,
    ProductComponentUpdateSerializer,
    ProductComponentResponseSerializer,
)
from .resource import ResourceResponseSerializer, ResourceCreateSerializer, ResourceUpdateSerializer
from .warehouse import WarehouseResponseModelSerializer, WarehouseCreateModelSerializer, WarehouseUpdateModelSerializer
from .file_attachment import FileAttachmentSerializer

__all__ = [
    'WarehouseResponseModelSerializer',
    'WarehouseCreateModelSerializer',
    'WarehouseUpdateModelSerializer',
    'FileAttachmentSerializer',
    'CategoryCreateSerializer',
    'CategoryResponseSerializer',
    'MaterialCreateSerializer',
    'MaterialUpdateSerializer',
    'MaterialResponseSerializer',
    'ResourceResponseSerializer',
    'ResourceCreateSerializer',
    'ResourceUpdateSerializer',
    'ProductComponentCreateSerializer',
    'ProductComponentUpdateSerializer',
    'ProductComponentResponseSerializer',
    'ProductCreateSerializer',
    'ProductUpdateSerializer',
    'ProductDetailSerializer',
    'ProductListSerializer',
]
