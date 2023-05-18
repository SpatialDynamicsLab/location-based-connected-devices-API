import logging
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api.serializers import (
    DeviceDataInputSerializer,
    DeviceDataOutputSerializer,
)
from api.models import DeviceData

logger = logging.getLogger(__name__)


class APIRootView(APIView):
    def get(self, request):
        response_data = {
            "API status": "Alive",
            "devices-data": request.build_absolute_uri('/api/v1/devices-data'),
        }
        return Response(response_data)


class DeviceDataView(ModelViewSet):
    http_method_names = ["post", "get", "put"]
    queryset = DeviceData.objects.all()
    serializer_classes = {
        "create": DeviceDataInputSerializer,
        "list": DeviceDataOutputSerializer,
        "retrieve": DeviceDataOutputSerializer,
        "update": DeviceDataInputSerializer,
    }

    default_serializer_class = DeviceDataOutputSerializer

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

