from django_filters import rest_framework as filters
from api.models import DeviceData


class DatesFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(
        field_name='location_timeStamp', lookup_expr='date__gte')
    end_date = filters.DateTimeFilter(
        field_name='location_timeStamp', lookup_expr='date__lte')
    date = filters.DateTimeFilter(
        field_name='location_timeStamp', lookup_expr='date'
    )

    class Meta:
        model = DeviceData
        fields = ('start_date', 'end_date', 'date', )


