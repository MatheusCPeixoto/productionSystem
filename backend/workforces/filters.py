import django_filters


class WorkforceFilter(django_filters.FilterSet):
    code = django_filters.NumberFilter(lookup_expr='exact')
    name = django_filters.CharFilter(lookup_expr='icontains')