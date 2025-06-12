from rest_framework import serializers
from .models import OrderActivityProgress, ActivityEquipmentLog, ActivityWorkforceLog, ActivityNonConformanceLog, WorkforceStoppageLog, EquipmentStoppageLog
from activitys.serializers import ActivitySerializer


class ActivityNonConformanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityNonConformanceLog
        fields = '__all__'


class ActivityEquipmentSerializer(serializers.ModelSerializer):
    equipment_description = serializers.CharField(source='equipment_code.description', read_only=True)

    class Meta:
        model = ActivityEquipmentLog
        fields = (
            'code',
            'equipment_code',
            'equipment_description',
            'start_date'
        )


class ActivityWorkforceSerializer(serializers.ModelSerializer):
    workforce_name = serializers.CharField(source='workforce_code.name', read_only=True)

    class Meta:
        model = ActivityWorkforceLog
        fields = (
            'code',
            'workforce_code',
            'workforce_name',
            'start_date'
        )


class OrderActivityProgressSerializer(serializers.ModelSerializer):
    # Campos aninhados (sua implementação está ótima)
    activity = ActivitySerializer(read_only=True)
    active_equipment_log = ActivityEquipmentSerializer(source='equipment_logs', many=True, read_only=True)
    active_workforce_log = ActivityWorkforceSerializer(source='workforce_logs', many=True, read_only=True)

    # Campo calculado (sua implementação está ótima)
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrderActivityProgress
        # --- AJUSTE AQUI ---
        # Garantir que todos os campos usados pelo serializer e pelo frontend estejam listados.
        # Adicionei 'company_code' e 'branch_code' que seu frontend usava para iniciar novos apontamentos.
        fields = (
            'code',
            'order_code',
            'activity',
            'sequence',
            'start_date',
            'end_date',
            'quantity',
            'status',
            'active_equipment_log',
            'active_workforce_log',
            'company_code',  # Adicionado para frontend
            'branch_code',  # Adicionado para frontend
        )

    def get_status(self, obj: OrderActivityProgress) -> str:
        # Sua implementação aqui está perfeita, sem necessidade de alterações.
        if obj.end_date is not None:
            return "Finalizado"

        has_open_workforce_stop = WorkforceStoppageLog.objects.filter(order_activity=obj,
                                                                      end_date__isnull=True).exists()
        has_open_equipment_stop = EquipmentStoppageLog.objects.filter(order_activity=obj,
                                                                      end_date__isnull=True).exists()

        if has_open_workforce_stop or has_open_equipment_stop:
            return "Parado"

        return "Em Andamento"
