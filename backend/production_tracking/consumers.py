# production_tracking/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Adiciona a conexão ao grupo 'terminals'
        await self.channel_layer.group_add(
            "terminals",
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        # Remove a conexão do grupo 'terminals'
        await self.channel_layer.group_discard(
            "terminals",
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name} with code {close_code}")

    # Método para receber mensagens do grupo 'terminals'
    async def task_update(self, event):
        # Envia a mensagem recebida do grupo para o WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'activity_id': event['activity_id'],
            'action': event['action'],
            # Incluir outros dados se necessário
        }))
        print(f"Sent message to WebSocket {self.channel_name}: {event}")

    # Você pode adicionar um método receive para lidar com mensagens do frontend,
    # mas para este caso (apenas receber atualizações do backend), não é estritamente necessário.
    # async def receive(self, text_data):
    #     pass # Não esperamos mensagens do cliente neste cenário