import django_filters


class ActivityEquipmentLogFilter(django_filters.FilterSet):
    order_activity = django_filters.NumberFilter(lookup_expr='exact')


class ActivityWorkforceLogFilter(django_filters.FilterSet):
    order_activity = django_filters.NumberFilter(lookup_expr='exact')


class OrderActivityProgressFilter(django_filters.FilterSet):
    order_code = django_filters.NumberFilter(lookup_expr='exact')
    activity_code = django_filters.NumberFilter(lookup_expr='exact')