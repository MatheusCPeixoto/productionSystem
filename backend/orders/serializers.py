from rest_framework import serializers
from .models import OrderItem
from structures.serializers import StructureActivitySerializer


class OrderItemSerializer(serializers.ModelSerializer):
    structure_activities = StructureActivitySerializer(
        source='structure_code.structure_activities',
        many=True,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = (
            'code',
            'order_code',
            'planned_quantity',
            'company_code',
            'branch_code',
            'structure_activities'
        )