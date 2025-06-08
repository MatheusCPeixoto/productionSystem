from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Equipment
from .serializers import EquipmentSerializer
from .filters import EquipmentFilter


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EquipmentFilter

