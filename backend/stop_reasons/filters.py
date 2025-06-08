import django_filters


class StopReasonFilter(django_filters.FilterSet):
    code = django_filters.NumberFilter(lookup_expr='exact')
    description = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.NumberFilter(lookup_expr='exact')