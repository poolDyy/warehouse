from rest_framework import routers

from api.v1.warehouse.views import (
    CategoryViewSet,
    FileAttachmentViewSet,
    MaterialViewSet,
    ProductComponentViewSet,
    ProductViewSet,
    ResourceViewSet,
    WarehouseViewSet,
)

app_name = 'warehouse'

router = routers.DefaultRouter()

router.register('file-attachment', FileAttachmentViewSet, basename='file-attachment')
router.register('category', CategoryViewSet, basename='category')
router.register('resources', ResourceViewSet, basename='resources')
router.register('products/(?P<product_id>[^/.]+)/components', ProductComponentViewSet, basename='components')
router.register('(?P<warehouse_id>[^/.]+)/products', ProductViewSet, basename='products')
router.register('(?P<warehouse_id>[^/.]+)/materials', MaterialViewSet, basename='materials')
router.register('', WarehouseViewSet, basename='warehouse-crud')

urlpatterns = router.urls
