from rest_framework import viewsets, status
from django.db import transaction
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


class StartActivityAppointmentView(APIView):

    def post(self, request, *args, **kwargs):
        # 1. Obter os dados da requisição do frontend
        data = request.data
        required_fields = [
            'company_code',
            'branch_code',
            'order_code',
            'activity_code',
            'sequence',
            'operator_code',
            'equipment_code'
        ]

        # 2. Validar se todos os campos necessários foram enviados
        for field in required_fields:
            if field not in data:
                return Response(
                    {'error': f'Campo obrigatório ausente: {field}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            # 3. Envolver tudo em uma transação atômica
            with transaction.atomic():
                # Busca objetos relacionados para garantir que os códigos são válidos
                # (Ajuste os modelos e campos conforme sua estrutura real)
                activity_obj = Activity.objects.get(code=data['activity_code'])
                operator_obj = Workforce.objects.get(code=data['operator_code'])
                equipment_obj = Equipment.objects.get(code=data['equipment_code'])

                # 4. POST 1: Criar o OrderActivityProgress
                new_progress = OrderActivityProgress.objects.create(
                    company_code_id=data['company_code'],  # Use '_id' se o campo for ForeignKey
                    branch_code_id=data['branch_code'],
                    order_code_id=data['order_code'],
                    activity=activity_obj,
                    sequence=data['sequence'],
                    start_date=timezone.now()  # Use o timezone do Django para consistência
                )

                # 5. POST 2: Criar o ActivityEquipmentLog
                ActivityEquipmentLog.objects.create(
                    order_activity=new_progress,  # Link com o objeto criado acima
                    equipment_code=equipment_obj,
                    start_date=timezone.now()
                )

                # 6. POST 3: Criar o ActivityWorkforceLog
                ActivityWorkforceLog.objects.create(
                    order_activity=new_progress,  # Link com o objeto criado acima
                    workforce_code=operator_obj,
                    start_date=timezone.now()
                )

                # 7. Retornar uma resposta de sucesso
                # Opcional: você pode serializar o objeto `new_progress` se o frontend precisar dele
                return Response(
                    {'message': 'Apontamento iniciado com sucesso!', 'progress_code': new_progress.code},
                    status=status.HTTP_201_CREATED
                )

        except Activity.DoesNotExist:
            return Response({'error': f"Atividade com código {data['activity_code']} não encontrada."},
                            status=status.HTTP_404_NOT_FOUND)
        except Workforce.DoesNotExist:
            return Response({'error': f"Operador com código {data['operator_code']} não encontrado."},
                            status=status.HTTP_404_NOT_FOUND)
        except Equipment.DoesNotExist:
            return Response({'error': f"Equipamento com código {data['equipment_code']} não encontrado."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Captura qualquer outro erro que possa ocorrer durante o processo
            return Response({'error': f'Ocorreu um erro interno: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class OrderActivityProgressViewSet(viewsets.ModelViewSet):
    serializer_class = OrderActivityProgressSerializer

    def get_queryset(self):
        return OrderActivityProgress.objects.all().select_related('activity').prefetch_related(
            'equipment_logs',
            'workforce_logs'
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Sobrescreve o método PATCH para finalizar o apontamento e seus logs relacionados.
        """
        try:
            # Envolve todas as operações do banco de dados em uma transação
            with transaction.atomic():
                # 1. Atualiza o OrderActivityProgress principal
                instance = self.get_object()  # Pega o objeto pelo 'code'/'pk' na URL
                instance.quantity = request.data.get('quantity')
                instance.end_date = timezone.now()
                instance.status = 'Finalizado'  # Atualiza o status
                instance.save()

                data_e_hora_atuais = instance.end_date

                # 2. Atualiza o ActivityWorkforceLog relacionado
                # Encontra todos os logs de mão de obra para este apontamento que ainda não têm data final
                ActivityWorkforceLog.objects.filter(
                    order_activity=instance,
                    end_date__isnull=True
                ).update(end_date=data_e_hora_atuais)

                # 3. Atualiza o ActivityEquipmentLog relacionado
                # Você mencionou EquipmentStoppageLog, mas estou usando ActivityEquipmentLog
                # para manter a consistência com a criação. Ajuste se o modelo for outro.
                ActivityEquipmentLog.objects.filter(
                    order_activity=instance,
                    end_date__isnull=True
                ).update(end_date=data_e_hora_atuais)

                # Serializa a instância atualizada para retornar ao frontend
                serializer = self.get_serializer(instance)
                return Response(serializer.data)

        except Exception as e:
            return Response(
                {'error': f'Ocorreu um erro interno ao finalizar o apontamento: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='start')
    def start_activity(self, request, *args, **kwargs):
        """
        Endpoint único para iniciar um apontamento de atividade.
        (A MESMA LÓGICA DA SUA StartActivityAppointmentView.post() VEM AQUI)
        """
        data = request.data
        # ... (validação dos dados)
        try:
            with transaction.atomic():
                # ... (criação dos 3 objetos no banco)
                return Response({'message': 'Apontamento iniciado com sucesso!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='stop')
    def stop(self, request, pk=None):
        """
        Ação para parar um apontamento.
        Cria logs de parada para todos os operadores e equipamentos ativos.
        """
        activity_progress = self.get_object()  # Pega o apontamento pelo ID (pk) na URL
        stop_reason_code = request.data.get('stop_reason_code')

        if not stop_reason_code:
            return Response({'error': 'O código do motivo da parada é obrigatório.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            stop_reason = StopReason.objects.get(code=stop_reason_code)

            with transaction.atomic():
                # 1. Altera o status do apontamento principal para "Parado"
                activity_progress.status = 'Parado'
                activity_progress.save()

                data_e_hora_atuais = timezone.now()

                # 2. Cria logs de parada para TODOS os operadores ativos no apontamento
                active_workforce = ActivityWorkforceLog.objects.filter(order_activity=activity_progress,
                                                                       end_date__isnull=True)
                for log in active_workforce:
                    # NOTA: Aqui você pode adicionar lógica para não criar uma nova parada se já houver uma aberta
                    WorkforceStoppageLog.objects.create(
                        order_activity=activity_progress,
                        workforce_code=log.workforce_code,
                        stop_reason_code=stop_reason,
                        start_date=data_e_hora_atuais
                    )

                # 3. Cria logs de parada para TODOS os equipamentos ativos
                active_equipment = ActivityEquipmentLog.objects.filter(order_activity=activity_progress,
                                                                       end_date__isnull=True)
                # Você mencionou EquipmentStoppageLog. Se o modelo for outro, ajuste o nome.
                for log in active_equipment:
                    EquipmentStoppageLog.objects.create(
                        order_activity=activity_progress,
                        equipment_code=log.equipment_code,
                        stop_reason_code=stop_reason,
                        start_date=data_e_hora_atuais
                    )

            return Response({'message': 'Apontamento parado com sucesso.'}, status=status.HTTP_200_OK)

        except StopReason.DoesNotExist:
            return Response({'error': 'Motivo da parada inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Erro ao processar parada: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='resume')
    def resume(self, request, pk=None):
        """
        Ação para retomar um apontamento parado.
        Finaliza (coloca end_date) nos logs de parada abertos.
        """
        activity_progress = self.get_object()

        try:
            with transaction.atomic():
                # 1. Altera o status do apontamento principal de volta para "Em Andamento"
                activity_progress.status = 'Em Andamento'
                activity_progress.save()

                data_e_hora_atuais = timezone.now()

                # 2. Fecha todos os logs de parada de mão de obra abertos para este apontamento
                WorkforceStoppageLog.objects.filter(
                    order_activity=activity_progress,
                    end_date__isnull=True
                ).update(end_date=data_e_hora_atuais)

                # 3. Fecha todos os logs de parada de equipamento abertos
                EquipmentStoppageLog.objects.filter(
                    order_activity=activity_progress,
                    end_date__isnull=True
                ).update(end_date=data_e_hora_atuais)

            return Response({'message': 'Apontamento retomado com sucesso.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Erro ao processar retomada: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)