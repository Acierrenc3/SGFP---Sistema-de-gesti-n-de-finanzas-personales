// Servicio de WebSocket para notificaciones en tiempo real
// Basado en: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

import { useNotificacionesStore } from '../stores/notificaciones'
import { useAutenticacionStore } from '../stores/autenticacion'

const URL_WS = (import.meta.env.VITE_API_URL || 'http://localhost:8000')
  .replace('https://', 'wss://')
  .replace('http://', 'ws://')

let websocket = null
let intervaloReconexion = null
let intentosReconexion = 0
const MAX_INTENTOS = 5
const DELAY_RECONEXION = 3000

export function conectarWebSocket() {
  const autenticacion = useAutenticacionStore()

  if (!autenticacion.token) return
  if (websocket?.readyState === WebSocket.OPEN) return

  try {
    websocket = new WebSocket(`${URL_WS}/ws/${autenticacion.token}`)

    websocket.onopen = () => {
      console.log('WebSocket conectado')
      intentosReconexion = 0
      if (intervaloReconexion) {
        clearInterval(intervaloReconexion)
        intervaloReconexion = null
      }
      // Ping cada 30 segundos para mantener la conexión viva
      intervaloReconexion = setInterval(() => {
        if (websocket?.readyState === WebSocket.OPEN) {
          websocket.send('ping')
        }
      }, 30000)
    }

    websocket.onmessage = (evento) => {
      try {
        const datos = JSON.parse(evento.data)
        manejarMensaje(datos)
      } catch {
        // Mensaje de texto plano (pong)
      }
    }

    websocket.onclose = () => {
      console.log('WebSocket desconectado')
      if (intervaloReconexion) {
        clearInterval(intervaloReconexion)
        intervaloReconexion = null
      }
      // Reconexión automática
      if (intentosReconexion < MAX_INTENTOS && autenticacion.token) {
        intentosReconexion++
        setTimeout(() => conectarWebSocket(), DELAY_RECONEXION)
      }
    }

    websocket.onerror = () => {
      websocket?.close()
    }

  } catch (error) {
    console.error('Error al conectar WebSocket:', error)
  }
}

export function desconectarWebSocket() {
  if (intervaloReconexion) {
    clearInterval(intervaloReconexion)
    intervaloReconexion = null
  }
  if (websocket) {
    websocket.close()
    websocket = null
  }
  intentosReconexion = MAX_INTENTOS
}

function manejarMensaje(datos) {
  const notificaciones = useNotificacionesStore()

  switch (datos.tipo) {
    case 'presupuesto_superado':
    case 'presupuesto_alerta':
    case 'presupuesto_info':
      notificaciones.agregarNotificacionWS({
        id: Date.now(),
        categoria: datos.categoria,
        mensaje: datos.mensaje,
        porcentaje: datos.porcentaje,
        icono: datos.icono,
        tipo: datos.nivel
      })
      break
    case 'conexion':
      console.log('WebSocket:', datos.mensaje)
      break
  }
}