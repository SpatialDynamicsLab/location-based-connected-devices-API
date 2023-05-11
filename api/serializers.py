import logging
from datetime import datetime
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point

from api.models import DeviceData

logger = logging.getLogger(__name__)


class DeviceDataInputSerializer(ModelSerializer):

    location_latitude = serializers.FloatField(write_only=True)
    location_longitude = serializers.FloatField(write_only=True)
    location_timeStamp = serializers.IntegerField(write_only=True)

    class Meta:
        model = DeviceData
        fields = (
            'identifier',
            'name',
            'location_latitude',
            'location_longitude',
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
            'latitude',
            'longitude',
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
