from django.urls import path, include
from rest_framework import routers
from django.conf import settings

from api.views import (
    APIRootView,
    DeviceDataView,
    DeviceGeoJSONView,
    DeviceGeoJSONDownloadView,
    DeviceCSVDownloadView,
)

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(
    '', DeviceDataView, basename='devices-data'
)


app_name = 'devices-data'
urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('devices/data/', include(router.urls)),
    path('devices/geojson/',
         DeviceGeoJSONView.as_view(), name='device-data-geojson'),
    path('devices/geojson/download/',
         DeviceGeoJSONDownloadView.as_view(),
         name='device-data-geojson-download'
         ),
    path('devices/csv/download/',
         DeviceCSVDownloadView.as_view(),
         name='device-data-csv-download'
         ),
]
