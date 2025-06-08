import django_filters


class OrderItemFilter(django_filters.FilterSet):
    order_code = django_filters.NumberFilter(field_name='order_code', lookup_expr='exact')