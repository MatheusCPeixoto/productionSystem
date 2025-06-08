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
    activity = ActivitySerializer(
        read_only=True
    )
    active_equipment_log = ActivityEquipmentSerializer(
        source='equipment_logs', # Muito mais limpo!
        many=True,
        read_only=True
    )
    active_workforce_log = ActivityWorkforceSerializer(
        source='workforce_logs', # Muito mais limpo!
        many=True,
        read_only=True
    )

    status = serializers.SerializerMethodField()

    def get_status(self, obj: OrderActivityProgress) -> str:
        """
        Calcula o status real do apontamento com base na nova regra.
        'obj' é a instância do OrderActivityProgress que está sendo serializada.
        """
        # 1. Se o apontamento já tem uma data de fim, ele está finalizado.
        if obj.end_date is not None:
            return "Finalizado"

        # 2. Se não está finalizado, verifica se há alguma parada aberta.
        #    Verifica se existe algum log de parada (de operador OU de equipamento)
        #    ligado a este apontamento que NÃO tenha end_date.
        has_open_workforce_stop = WorkforceStoppageLog.objects.filter(order_activity=obj,
                                                                      end_date__isnull=True).exists()
        has_open_equipment_stop = EquipmentStoppageLog.objects.filter(order_activity=obj,
                                                                      end_date__isnull=True).exists()

        if has_open_workforce_stop or has_open_equipment_stop:
            return "Parado"

        # 3. Se não está finalizado e não tem paradas abertas, está em andamento.
        return "Em Andamento"

    class Meta:
        model = OrderActivityProgress
        fields = (
            'code',
            'order_code',
            'activity',
            'sequence',
            'start_date',
            'end_date',
            'quantity',
            'status',
            'active_equipment_log',  # Nomes mantidos
            'active_workforce_log'   # Nomes mantidos
        )

