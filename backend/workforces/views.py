from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Workforce
from .serializers import WorkforceSerializer
from .filters import WorkforceFilter


class WorkforceViewSet(viewsets.ModelViewSet):
    queryset = Workforce.objects.all()
    serializer_class = WorkforceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkforceFilter

