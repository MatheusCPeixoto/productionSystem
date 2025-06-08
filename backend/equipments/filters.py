import django_filters


class EquipmentFilter(django_filters.FilterSet):
    code = django_filters.NumberFilter(lookup_expr='exact')
    description = django_filters.CharFilter(lookup_expr='icontains')
    equipment_id = django_filters.CharFilter(lookup_expr='icontains')

