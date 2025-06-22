import django_filters


class ProductFilter(django_filters.FilterSet):
    code = django_filters.NumberFilter(field_name='code', lookup_expr='exact')
    identifier = django_filters.CharFilter(field_name='product_identifier', lookup_expr='icontains')