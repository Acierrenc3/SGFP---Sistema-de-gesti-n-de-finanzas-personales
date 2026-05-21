# Endpoint WebSocket para notificaciones en tiempo real
# Basado en: https://fastapi.tiangolo.com/advanced/websockets/

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import gestor_ws
from app.core.seguridad import decodificar_token
from app.db.sesion import obtener_sesion_sync
from app.modelos.usuario import Usuario

enrutador = APIRouter()


@enrutador.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    """
    Endpoint WebSocket autenticado mediante token JWT.
    El cliente se conecta enviando el token como parámetro de ruta.
    """
    # Verifica el token JWT
    payload = decodificar_token(token)
    if not payload:
        await websocket.close(code=4001)
        return

    email = payload.get("sub")
    if not email:
        await websocket.close(code=4001)
        return

    # Obtiene el usuario de la base de datos
    sesion = next(obtener_sesion_sync())
    usuario = sesion.query(Usuario).filter(Usuario.email == email).first()
    sesion.close()

    if not usuario:
        await websocket.close(code=4001)
        return

    # Conecta al usuario
    await gestor_ws.conectar(websocket, usuario.id)

    try:
        # Envía mensaje de bienvenida
        await gestor_ws.enviar_a_usuario(usuario.id, {
            "tipo": "conexion",
            "mensaje": "Conectado al servidor de notificaciones"
        })

        # Mantiene la conexión abierta esperando mensajes
        while True:
            # Espera mensajes del cliente (ping/pong)
            datos = await websocket.receive_text()
            if datos == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        gestor_ws.desconectar(usuario.id)