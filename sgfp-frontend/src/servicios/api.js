// Cliente HTTP Axios para consumir la API REST
// Basado en: https://axios-http.com/docs/instance

import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
    headers: {
        'Content-Type': 'application/json'
    }
})

// Interceptor de peticiones: añade el token JWT
api.interceptors.request.use(
    (configuracion) => {
        const token = localStorage.getItem('token')
        if (token) {
            configuracion.headers.Authorization = `Bearer ${token}`
        }
        return configuracion
    },
    (error) => Promise.reject(error)
)

// Interceptor de respuestas: renueva el token si expira (401)
api.interceptors.response.use(
    (respuesta) => respuesta,
    async (error) => {
        const peticionOriginal = error.config

        // Si el token expiró y no hemos intentado renovarlo aún
        if (error.response?.status === 401 && !peticionOriginal._reintentado) {
            peticionOriginal._reintentado = true

            try {
                // Importa el store dinámicamente para evitar dependencias circulares
                const { useAutenticacionStore } = await import('../stores/autenticacion')
                const autenticacion = useAutenticacionStore()

                const nuevoToken = await autenticacion.renovarToken()

                if (nuevoToken) {
                    // Reintenta la petición original con el nuevo token
                    peticionOriginal.headers.Authorization = `Bearer ${nuevoToken}`
                    return api(peticionOriginal)
                }
            } catch {
                // Si falla el refresh, redirige al login
                localStorage.removeItem('token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('usuario')
                window.location.href = '/inicio-sesion'
            }
        }

        return Promise.reject(error)
    }
)

export default api