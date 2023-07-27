import logging
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_csv.renderers import CSVRenderer
from api.filters import DatesFilter

from api.serializers import (
    DeviceDataInputSerializer,
    DeviceDataOutputSerializer,
    DeviceDataCSVSerializer
)
from api.models import DeviceData

logger = logging.getLogger(__name__)


class APIRootView(APIView):
    def get(self, request):
        response_data = {
            "API status": "Alive",
            "devices-data": {
                "geojson-api": request.build_absolute_uri(
                    '/api/v1/devices/data/'),
                "geojson": request.build_absolute_uri(
                    '/api/v1/devices/geojson/'),
                "geojson-download": request.build_absolute_uri(
                              '/api/v1/devices/geojson/download/'),
                "csv-download": request.build_absolute_uri(
                    '/api/v1/devices/csv/download/'),
            }
        }
        return Response(response_data)


class DeviceDataView(ModelViewSet):
    http_method_names = ["post", "get", "put"]
    # queryset = DeviceData.objects.all()
    serializer_classes = {
        "create": DeviceDataInputSerializer,
        "list": DeviceDataOutputSerializer,
        "retrieve": DeviceDataOutputSerializer,
        "update": DeviceDataInputSerializer,
    }
    default_serializer_class = DeviceDataOutputSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = DatesFilter

    def get_queryset(self):
        queryset = DeviceData.objects.all()
        filter_params = self.request.GET.copy()
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'today':
            # If 'fileter' is 'today', get today's date
            today = datetime.now().date()
            filter_params['date'] = today
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'week':
            past_week_start_date = datetime.now().date() - timedelta(days=7)
            filter_params = {
                'start_date': past_week_start_date,
                'end_date': datetime.now().date(),
            }
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'month':
            past_month_start_date = datetime.now().date() - timedelta(days=30)
            filter_params = {
                'start_date': past_month_start_date,
                'end_date': datetime.now().date(),
            }
        location_filter = DatesFilter(filter_params, queryset=queryset)
        if location_filter.is_valid():
            queryset = location_filter.qs
        return queryset

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(
                data=request.data
            )
            if serializer.is_valid():
                instance = serializer.create(serializer.validated_data)
                # instance = serializer.save()
                return Response({
                    'success': True,
                    'data': self.default_serializer_class(instance).data},
                    status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            logger.error(ex)
            return Response({
                'success': False,
                'message': str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeviceGeoJSONView(APIView):

    def get_queryset(self):
        queryset = DeviceData.objects.all()
        filter_params = self.request.GET.copy()
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'today':
            # If 'fileter' is 'today', get today's date
            today = datetime.now().date()
            filter_params['date'] = today
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'week':
            past_week_start_date = datetime.now().date() - timedelta(days=7)
            filter_params = {
                'start_date': past_week_start_date,
                'end_date': datetime.now().date(),
            }
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'month':
            past_month_start_date = datetime.now().date() - timedelta(days=30)
            filter_params = {
                'start_date': past_month_start_date,
                'end_date': datetime.now().date(),
            }
        location_filter = DatesFilter(filter_params, queryset=queryset)
        if location_filter.is_valid():
            queryset = location_filter.qs
        return queryset

    def get(self, request):
        device_data = self.get_queryset()
        serializer = DeviceDataOutputSerializer(device_data, many=True)
        response = Response(serializer.data, content_type='application/json')
        return response


class DeviceGeoJSONDownloadView(APIView):

    def get_queryset(self):
        queryset = DeviceData.objects.all()
        filter_params = self.request.GET.copy()
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'today':
            # If 'fileter' is 'today', get today's date
            today = datetime.now().date()
            filter_params['date'] = today
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'week':
            past_week_start_date = datetime.now().date() - timedelta(days=7)
            filter_params = {
                'start_date': past_week_start_date,
                'end_date': datetime.now().date(),
            }
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'month':
            past_month_start_date = datetime.now().date() - timedelta(days=30)
            filter_params = {
                'start_date': past_month_start_date,
                'end_date': datetime.now().date(),
            }
        location_filter = DatesFilter(filter_params, queryset=queryset)
        if location_filter.is_valid():
            queryset = location_filter.qs
        return queryset

    def get(self, request):
        device_data = self.get_queryset()
        serializer = DeviceDataOutputSerializer(device_data, many=True)
        response = Response(serializer.data, content_type='application/geojson')
        response['Content-Disposition'] =\
            'attachment; filename="devices-data.geojson"'
        return response


class DeviceCSVDownloadView(APIView):
    renderer_classes = [CSVRenderer]

    def get_queryset(self):
        queryset = DeviceData.objects.all()
        filter_params = self.request.GET.copy()
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'today':
            # If 'fileter' is 'today', get today's date
            today = datetime.now().date()
            filter_params['date'] = today
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'week':
            past_week_start_date = datetime.now().date() - timedelta(days=7)
            filter_params = {
                'start_date': past_week_start_date,
                'end_date': datetime.now().date(),
            }
        if 'filter' in filter_params \
                and filter_params['filter'].lower() == 'month':
            past_month_start_date = datetime.now().date() - timedelta(days=30)
            filter_params = {
                'start_date': past_month_start_date,
                'end_date': datetime.now().date(),
            }
        location_filter = DatesFilter(filter_params, queryset=queryset)
        if location_filter.is_valid():
            queryset = location_filter.qs
        return queryset

    def get(self, request):
        device_data = self.get_queryset()
        serializer = DeviceDataCSVSerializer(device_data, many=True)
        response = Response(serializer.data, content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="devices-data.csv"'
        return response


