from rest_framework import viewsets, status
from django.db import transaction
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.decorators import action

from .models import OrderActivityProgress, ActivityEquipmentLog, ActivityWorkforceLog, ActivityNonConformanceLog, WorkforceStoppageLog, EquipmentStoppageLog
from .serializers import OrderActivityProgressSerializer, ActivityNonConformanceLogSerializer
from activitys.models import Activity # Exemplo de onde o modelo Activity pode estar
from enterprises.models import Company, Branch # Exemplo
from orders.models import Order # Exemplo
from workforces.models import Workforce # Exemplo
from equipments.models import Equipment # Exemplo
from stop_reasons.models import StopReason


class ActivityNonConformanceViewSet(viewsets.ModelViewSet):
    queryset = ActivityNonConformanceLog.objects.all()
    serializer_class = ActivityNonConformanceLogSerializer


class OrderActivityProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet final para gerenciar Apontamentos, com lógica para Múltipla Ordem,
    parada, retomada e finalização.
    """
    serializer_class = OrderActivityProgressSerializer
    # O queryset principal que lista os apontamentos
    queryset = OrderActivityProgress.objects.all().order_by('-start_date')

    # Método auxiliar privado para reutilizar a lógica de parada
    def _perform_stop_logic(self, activity_progress, stop_reason):
        if activity_progress.status == 'Parado':
            return  # Já está parado, não faz nada

        activity_progress.status = 'Parado'
        activity_progress.save()
        data_e_hora_atuais = timezone.now()

        active_workforce = ActivityWorkforceLog.objects.filter(order_activity=activity_progress, end_date__isnull=True)
        for log in active_workforce:
            WorkforceStoppageLog.objects.create(order_activity=activity_progress, workforce_code=log.workforce_code,
                                                stop_reason_code=stop_reason, start_date=data_e_hora_atuais)

        active_equipment = ActivityEquipmentLog.objects.filter(order_activity=activity_progress, end_date__isnull=True)
        for log in active_equipment:
            EquipmentStoppageLog.objects.create(order_activity=activity_progress, equipment_code=log.equipment_code,
                                                stop_reason_code=stop_reason, start_date=data_e_hora_atuais)

    # Ação customizada para INICIAR um novo apontamento
    @action(detail=False, methods=['post'], url_path='start')
    def start_activity(self, request, *args, **kwargs):
        data = request.data
        required_fields = ['company_code', 'branch_code', 'order_code', 'activity_code', 'sequence', 'operator_code',
                           'equipment_code']
        if any(field not in data for field in required_fields):
            return Response({'error': 'Campos obrigatórios ausentes.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                operator_code = data['operator_code']
                equipment_code = data['equipment_code']

                # --- LÓGICA DE MÚLTIPLA ORDEM ATUALIZADA ---
                # Apenas executa se o frontend indicar que o modo está ativo
                if data.get('multi_order_mode') is True:
                    # Filtra tarefas ativas que sejam do mesmo operador OU do mesmo equipamento
                    tasks_to_stop = OrderActivityProgress.objects.filter(
                        Q(workforce_logs__workforce_code__code=operator_code) |
                        Q(equipment_logs__equipment_code__code=equipment_code),
                        status='Em Andamento'
                    ).distinct()

                    if tasks_to_stop.exists():
                        stop_reason_auto = StopReason.objects.get(code=20)
                        for task in tasks_to_stop:
                            self._perform_stop_logic(task, stop_reason_auto)
                # --- FIM DA LÓGICA DE MÚLTIPLA ORDEM ---

                activity_obj = Activity.objects.get(code=data['activity_code'])
                operator_obj = Workforce.objects.get(code=data['operator_code'])
                equipment_obj = Equipment.objects.get(code=data['equipment_code'])
                order_obj = Order.objects.get(code=data['order_code'])
                company_obj = Company.objects.get(code=data['company_code'])
                branch_obj = Branch.objects.get(code=data['branch_code'])

                new_progress = OrderActivityProgress.objects.create(
                    company_code=company_obj, branch_code=branch_obj, order_code=order_obj,
                    activity=activity_obj, sequence=data['sequence'],
                    start_date=timezone.now(), status='Em Andamento'
                )
                ActivityEquipmentLog.objects.create(order_activity=new_progress, equipment_code=equipment_obj,
                                                    start_date=timezone.now())
                ActivityWorkforceLog.objects.create(order_activity=new_progress, workforce_code=operator_obj,
                                                    start_date=timezone.now())

                serializer = self.get_serializer(new_progress)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except (StopReason.DoesNotExist, Activity.DoesNotExist, Workforce.DoesNotExist, Equipment.DoesNotExist,
                Order.DoesNotExist, Company.DoesNotExist, Branch.DoesNotExist) as e:
            return Response({'error': f"Um código fornecido é inválido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro interno: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Ação customizada para PARAR um apontamento
    @action(detail=True, methods=['post'], url_path='stop')
    def stop(self, request, pk=None):
        activity_progress = self.get_object()
        stop_reason_code = request.data.get('stop_reason_code')
        if not stop_reason_code:
            return Response({'error': 'O código do motivo da parada é obrigatório.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            stop_reason = StopReason.objects.get(code=stop_reason_code)
            self._perform_stop_logic(activity_progress, stop_reason)
            return Response({'message': 'Apontamento parado com sucesso.'}, status=status.HTTP_200_OK)
        except StopReason.DoesNotExist:
            return Response({'error': 'Motivo da parada inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Erro ao processar parada: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Ação customizada para RETOMAR um apontamento
    @action(detail=True, methods=['post'], url_path='resume')
    def resume(self, request, pk=None):
        activity_to_resume = self.get_object()
        try:
            with transaction.atomic():
                # --- LÓGICA DE MÚLTIPLA ORDEM ATUALIZADA ---
                if request.data.get('multi_order_mode') is True:
                    current_logs_op = activity_to_resume.workforce_logs.all()
                    current_logs_eq = activity_to_resume.equipment_logs.all()
                    if current_logs_op.exists() or current_logs_eq.exists():
                        operator_codes = [log.workforce_code.code for log in current_logs_op]
                        equipment_codes = [log.equipment_code.code for log in current_logs_eq]
                        tasks_to_stop = OrderActivityProgress.objects.filter(
                            Q(workforce_logs__workforce_code__code__in=operator_codes) |
                            Q(equipment_logs__equipment_code__code__in=equipment_codes),
                            status='Em Andamento'
                        ).exclude(pk=activity_to_resume.pk).distinct()
                        if tasks_to_stop.exists():
                            stop_reason_auto = StopReason.objects.get(code=20)
                            for task in tasks_to_stop:
                                self._perform_stop_logic(task, stop_reason_auto)
                # --- FIM DA LÓGICA DE MÚLTIPLA ORDEM ---

                activity_to_resume.status = 'Em Andamento'
                activity_to_resume.save()
                data_e_hora_atuais = timezone.now()
                WorkforceStoppageLog.objects.filter(order_activity=activity_to_resume, end_date__isnull=True).update(
                    end_date=data_e_hora_atuais)
                EquipmentStoppageLog.objects.filter(order_activity=activity_to_resume, end_date__isnull=True).update(
                    end_date=data_e_hora_atuais)

            return Response({'message': 'Apontamento retomado com sucesso.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Erro ao processar retomada: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Método PATCH para FINALIZAR um apontamento
    def partial_update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                if instance.status == 'Parado':
                    data_e_hora_atuais = timezone.now()
                    WorkforceStoppageLog.objects.filter(order_activity=instance, end_date__isnull=True).update(
                        end_date=data_e_hora_atuais)
                    EquipmentStoppageLog.objects.filter(order_activity=instance, end_date__isnull=True).update(
                        end_date=data_e_hora_atuais)

                instance.quantity = request.data.get('quantity')
                instance.end_date = timezone.now()
                instance.status = 'Finalizado'
                instance.save()
                ActivityWorkforceLog.objects.filter(order_activity=instance, end_date__isnull=True).update(
                    end_date=instance.end_date)
                ActivityEquipmentLog.objects.filter(order_activity=instance, end_date__isnull=True).update(
                    end_date=instance.end_date)
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro interno ao finalizar: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)