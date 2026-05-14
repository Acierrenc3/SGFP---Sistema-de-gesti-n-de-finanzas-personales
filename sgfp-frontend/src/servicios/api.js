// Cliente HTTP Axios para consumir la API REST
// Basado en: https://axios-http.com/docs/instance

import axios from 'axios'

// Crea una instancia de Axios con la URL base de la API
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
    headers: {
        'Content-Type': 'application/json'
    }
})

// Interceptor de peticiones
// Añade el token JWT a cada petición automáticamente
// Basado en: https://axios-http.com/docs/interceptors
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

// Interceptor de respuestas
// Maneja errores globales de autenticación (401)
api.interceptors.response.use(
    (respuesta) => respuesta,
    (error) => {
        // Si el token expiró o es inválido, limpia la sesión
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            localStorage.removeItem('usuario')
            window.location.href = '/inicio-sesion'
        }
        return Promise.reject(error)
    }
)

export default api