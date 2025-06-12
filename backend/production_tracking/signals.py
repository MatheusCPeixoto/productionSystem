# production_tracking/signals.py

from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import OrderActivityProgress, ActivityWorkforceLog, ActivityEquipmentLog, ActivityNonConformanceLog
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Função auxiliar para enviar a mensagem via WebSocket
def send_task_update(activity_id, action_type):
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            "terminals", # Nome do grupo que os terminais se conectarão
            {
                "type": "task_update", # Nome do método no Consumer (task_update)
                "activity_id": str(activity_id),
                "action": action_type, # Ex: 'saved', 'deleted', 'log_changed'
                # Opcional: enviar dados parciais ou completos, ou apenas o ID para o frontend buscar
            }
        )

# Signal para OrderActivityProgress (status, quantity, dates)
@receiver(post_save, sender=OrderActivityProgress)
def order_activity_progress_saved(sender, instance, created, **kwargs):
    # Envia uma mensagem sempre que um OrderActivityProgress é salvo
    # O frontend pode então re-fetch a lista ou o item específico
    send_task_update(instance.code, 'saved')

@receiver(post_delete, sender=OrderActivityProgress)
def order_activity_progress_deleted(sender, instance, **kwargs):
    # Envia uma mensagem quando um OrderActivityProgress é deletado
    send_task_update(instance.code, 'deleted')

# Signals para os logs (operadores, equipamentos)
@receiver(post_save, sender=ActivityWorkforceLog)
def workforce_log_saved(sender, instance, created, **kwargs):
    # Quando um log de operador muda, a tarefa associada precisa ser atualizada
    if instance.order_activity:
        send_task_update(instance.order_activity.code, 'log_changed')

@receiver(post_delete, sender=ActivityWorkforceLog)
def workforce_log_deleted(sender, instance, **kwargs):
    if instance.order_activity:
        send_task_update(instance.order_activity.code, 'log_changed')

@receiver(post_save, sender=ActivityEquipmentLog)
def equipment_log_saved(sender, instance, created, **kwargs):
    if instance.order_activity:
        send_task_update(instance.order_activity.code, 'log_changed')

@receiver(post_delete, sender=ActivityEquipmentLog)
def equipment_log_deleted(sender, instance, **kwargs):
    if instance.order_activity:
        send_task_update(instance.order_activity.code, 'log_changed')

# Signal para Não Conformidades (se a NC afeta a exibição do cartão)
@receiver(post_save, sender=ActivityNonConformanceLog)
def nc_log_saved(sender, instance, created, **kwargs):
     if instance.order_activity:
        send_task_update(instance.order_activity.code, 'nc_added')

# Você precisaria garantir que esses sinais são carregados.
# Adicione `default_app_config = 'your_app_name.apps.YourAppConfig'`
# no seu __init__.py e defina ready() no apps.py