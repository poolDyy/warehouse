from rest_framework import routers

from api.v1.unit.views import UnitViewSet

app_name = 'unit'

router = routers.DefaultRouter()

router.register(r'', UnitViewSet, basename='unit')

urlpatterns = router.urls
