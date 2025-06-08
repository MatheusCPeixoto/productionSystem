from django.urls import path, include

from .views import OrderItemListView

urlpatterns = [
    path('order-items/', OrderItemListView.as_view(), name='order-item-list')
]