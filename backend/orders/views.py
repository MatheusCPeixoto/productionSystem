from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import OrderItem
from .serializers import OrderItemSerializer
from .filters import OrderItemFilter

class OrderItemListView(ListAPIView):
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderItemFilter

    def get_queryset(self):
        return OrderItem.objects.select_related('structure_code').prefetch_related('structure_code__structure_activities')