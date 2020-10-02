import django_filters

from .models import Complain


class ComplainFilter(django_filters.FilterSet):
    date_complain = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Complain
        fields = ['date_complain']
