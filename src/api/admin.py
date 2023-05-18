from django.contrib import admin
from api.models import DeviceData

# Register your models here.
admin.site.site_header = "UCD Spatial Dynamics Lab | " \
                         "Location-based connected devices API"


@admin.register(DeviceData)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        f.name for f in DeviceData._meta.fields
    ]
