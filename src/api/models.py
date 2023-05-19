from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class DeviceData(models.Model):
    identifier = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    location = models.PointField(
        _("location"),
        geography=True,
        null=False,
        blank=False
    )
    location_timeStamp = models.DateTimeField(
        null=False,
        blank=False
    )
    location_positionType = models.CharField(
        null=True,
        blank=True,
    )
    location_horizontalAccuracy = models.FloatField(
        null=True,
        blank=True,
    )
    location_verticalAccuracy = models.FloatField(
        null=True,
        blank=True,
    )
    location_isInaccurate = models.BooleanField(
        null=True,
        blank=True,
    )
    location_isOld = models.BooleanField(
        null=True,
        blank=True,
    )
    location_locationFinished = models.BooleanField(
        null=True,
        blank=True,
    )
    batteryLevel = models.FloatField(
        null=True,
        blank=True,
    )
    batteryStatus = models.CharField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Device Data")
        verbose_name_plural = _("Device Data")

    def __str__(self):
        return f"{self.name}"

    @property
    def longitude(self):
        return self.location.y

    @property
    def latitude(self):
        return self.location.x
