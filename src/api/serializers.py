import logging
from datetime import datetime
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point

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

        # for key, value in attrs.items():
        #     print(key)
        #     if isinstance(value, str) and value.isdigit() or value.isnumeric():
        #         attrs[key] = float(value)
        #     if isinstance(value, str) and \
        #             type(self.fields[key].model_field).__name__ == 'float':
        #         attrs[key] = None
        # return attrs

    def create(self, validated_data):
        try:
            device_id = validated_data.pop('device_id')
            if device_id and device_id != 'NULL':
                validated_data['identifier'] = device_id
            latitude = validated_data.pop('location_latitude')
            longitude = validated_data.pop('location_longitude')
            geom = Point(float(latitude), float(longitude))
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
