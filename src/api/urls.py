from django.urls import path, include
from rest_framework import routers
from django.conf import settings

# Local Libraries
from api.views import (
    APIRootView,
    DeviceDataView,
    DeviceCSVDownloadView
)

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(
    'devices', DeviceDataView, basename='devices-data')


app_name = 'devices-data'
urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('devices/csv/', DeviceCSVDownloadView.as_view(), name='device-data-csv'),
    path('', include(router.urls)),
]
