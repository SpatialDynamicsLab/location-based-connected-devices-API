from django.urls import path, include
from rest_framework import routers
from django.conf import settings

# Local Libraries
from api.views import (
    APIRootView,
    DeviceDataView
)

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(
    'devices-data', DeviceDataView, basename='devices-data')


app_name = 'devices-data'
urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('', include(router.urls)),
]
