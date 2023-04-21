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
    location_timestamp = models.DateTimeField(
        null=False,
        blank=False
    )
    location_position_type = models.CharField(
        null=True,
        blank=True,
    )
    location_horizontal_accuracy = models.FloatField(
        null=True,
        blank=True,
    )
    location_vertical_accuracy = models.FloatField(
        null=True,
        blank=True,
    )
    location_is_inaccurate = models.BooleanField(
        null=True,
        blank=True,
    )
    location_is_old = models.BooleanField(
        null=True,
        blank=True,
    )
    location_finished = models.BooleanField(
        null=True,
        blank=True,
    )
    battery_level = models.FloatField(
        null=True,
        blank=True,
    )
    battery_status = models.CharField(
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
        return self.location.x

    @property
    def latitude(self):
        return self.location.y
