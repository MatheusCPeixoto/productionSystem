from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import NonConformance
from .serializers import NonConformanceSerializer
from .filters import NonConformanceFilter


class NonConformanceViewSet(viewsets.ModelViewSet):
    queryset = NonConformance.objects.all()
    serializer_class = NonConformanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NonConformanceFilter

