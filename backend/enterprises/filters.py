import django_filters


class CompanyFilter(django_filters.FilterSet):
    code = django_filters.NumberFilter(lookup_expr='exact')
    name = django_filters.CharFilter(lookup_expr='icontains')
    cnpj = django_filters.CharFilter(lookup_expr='icontains')


class BranchFilter(django_filters.FilterSet):
    code = django_filters.NumberFilter(lookup_expr='exact')
    corporate_reason = django_filters.CharFilter(lookup_expr='icontains')
    cnpj = django_filters.CharFilter(lookup_expr='icontains')
