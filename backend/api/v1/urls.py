from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path(
        'users/',
        include('api.v1.users.urls', namespace='users'),
        name='users',
    ),
    path(
        'warehouse/',
        include('api.v1.warehouse.urls', namespace='warehouse'),
        name='warehouse',
    ),
    path(
        'units/',
        include('api.v1.unit.urls', namespace='units'),
        name='units',
    ),
]
