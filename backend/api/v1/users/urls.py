from rest_framework import routers

from api.v1.users.views import UserViewSet

app_name = 'users'

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)

urlpatterns = router.urls
