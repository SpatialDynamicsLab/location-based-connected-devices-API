import logging
from datetime import datetime
from django.contrib.gis.geos import Point
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_csv.renderers import CSVRenderer

from api.models import DeviceData

logger = logging.getLogger(__name__)


class DeviceDataInputSerializer(ModelSerializer):
    device_id = serializers.CharField(write_only=True, allow_null=True)
    location_latitude = serializers.FloatField(write_only=True)
    location_longitude = serializers.FloatField(write_only=True)
    location_timeStamp = serializers.IntegerField(write_only=True)

    class Meta:
        model = DeviceData
        fields = (
            'device_id',
            'identifier',
            'name',
            'location_longitude',
            'location_latitude',
            'location_timeStamp',
            'location_positionType',
            'location_horizontalAccuracy',
            'location_verticalAccuracy',
            'location_isInaccurate',
            'location_isOld',
            'location_locationFinished',
            'batteryLevel',
            'batteryStatus'
        )

    def create(self, validated_data):
        try:
            device_id = validated_data.pop('device_id')
            if device_id and device_id != 'NULL':
                validated_data['identifier'] = device_id
            longitude = validated_data.pop('location_longitude')
            latitude = validated_data.pop('location_latitude')
            geom = Point(float(longitude), float(latitude))
            validated_data['location'] = geom
            timestamp_data = validated_data.pop('location_timeStamp')
            if len(str(timestamp_data)) == 13:
                timestamp_data = datetime.fromtimestamp(
                    timestamp_data / 1000)
            else:
                timestamp_data = datetime.fromtimestamp(timestamp_data)
            validated_data['location_timeStamp'] = timestamp_data
            data = DeviceData.objects.create(**validated_data)
            return data
        except Exception as ex:
            logger.error(ex)
            raise serializers.ValidationError({'Error': ex})


class DeviceDataOutputSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = DeviceData
        geo_field = 'location'
        fields = (
            'id',
            'identifier',
            'name',
            'longitude',
            'latitude',
            'location_timeStamp',
            'location_positionType',
            'location_horizontalAccuracy',
            'location_verticalAccuracy',
            'location_isInaccurate',
            'location_isOld',
            'location_locationFinished',
            'batteryLevel',
            'batteryStatus'
        )


class DeviceDataCSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = (
            'id',
            'identifier',
            'name',
            'longitude',
            'latitude',
            'location_timeStamp',
            'location_positionType',
            'location_horizontalAccuracy',
            'location_verticalAccuracy',
            'location_isInaccurate',
            'location_isOld',
            'location_locationFinished',
            'batteryLevel',
            'batteryStatus'
        )
        csv_export = True
        csv_separator = ','

    @staticmethod
    def get_csv_renderer():
        return CSVRenderer()

    @staticmethod
    def get_csv_terminator():
        return '\r\n'
