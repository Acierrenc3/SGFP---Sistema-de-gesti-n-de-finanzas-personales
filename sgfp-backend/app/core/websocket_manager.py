# Gestor de conexiones WebSocket
# Basado en: https://fastapi.tiangolo.com/advanced/websockets/

from typing import Dict
from fastapi import WebSocket


class GestorWebSocket:
    """
    Gestiona las conexiones WebSocket activas de los usuarios.
    Permite enviar mensajes a usuarios específicos o a todos.
    """

    def __init__(self):
        # Diccionario de conexiones activas: {id_usuario: websocket}
        self.conexiones_activas: Dict[int, WebSocket] = {}

    async def conectar(self, websocket: WebSocket, id_usuario: int):
        """Acepta y registra una nueva conexión WebSocket."""
        await websocket.accept()
        self.conexiones_activas[id_usuario] = websocket

    def desconectar(self, id_usuario: int):
        """Elimina la conexión de un usuario."""
        if id_usuario in self.conexiones_activas:
            del self.conexiones_activas[id_usuario]

    async def enviar_a_usuario(self, id_usuario: int, mensaje: dict):
        """Envía un mensaje a un usuario específico."""
        if id_usuario in self.conexiones_activas:
            try:
                await self.conexiones_activas[id_usuario].send_json(mensaje)
            except Exception:
                self.desconectar(id_usuario)

    async def enviar_a_todos(self, mensaje: dict):
        """Envía un mensaje a todos los usuarios conectados."""
        desconectados = []
        for id_usuario, websocket in self.conexiones_activas.items():
            try:
                await websocket.send_json(mensaje)
            except Exception:
                desconectados.append(id_usuario)
        for id_usuario in desconectados:
            self.desconectar(id_usuario)


# Instancia global del gestor
gestor_ws = GestorWebSocket()