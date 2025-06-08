from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import StopReason
from .serializers import StopReasonSerializer
from .filters import StopReasonFilter

class StopReasonViewSet(viewsets.ModelViewSet):
    queryset = StopReason.objects.all()
    serializer_class = StopReasonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StopReasonFilter

