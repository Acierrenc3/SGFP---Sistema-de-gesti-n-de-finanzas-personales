// Store de autenticación con Pinia
// Basado en: https://pinia.vuejs.org/core-concepts/

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../servicios/api'

export const useAutenticacionStore = defineStore('autenticacion', () => {
    // Estado
    const token = ref(localStorage.getItem('token') || null)
    const refreshToken = ref(localStorage.getItem('refresh_token') || null)
    const usuario = ref(JSON.parse(localStorage.getItem('usuario') || 'null'))

    // Computed
    const estaAutenticado = computed(() => !!token.value)

    // Acciones
async function iniciarSesion(email, contrasena) {
    const axios = (await import('axios')).default

    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', contrasena)

    const respuesta = await axios.post(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/auth/token`,
        params,
        {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }
    )

    token.value = respuesta.data.access_token
    refreshToken.value = respuesta.data.refresh_token
    localStorage.setItem('token', token.value)
    localStorage.setItem('refresh_token', refreshToken.value)

    await obtenerPerfil()
}

    async function registrar(nombre, email, contrasena) {
        await api.post('/auth/registro', { nombre, email, contrasena })
    }

    async function obtenerPerfil() {
        const respuesta = await api.get('/usuarios/perfil')
        usuario.value = respuesta.data
        localStorage.setItem('usuario', JSON.stringify(usuario.value))
    }

    async function renovarToken() {
        "Renueva el token de acceso usando el refresh token"
        try {
            const axios = (await import('axios')).default

            const respuesta = await axios.post(
                `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/auth/refresh`,
                { refresh_token: refreshToken.value },
                { headers: { 'Content-Type': 'application/json' } }
            )

            token.value = respuesta.data.access_token
            refreshToken.value = respuesta.data.refresh_token
            localStorage.setItem('token', token.value)
            localStorage.setItem('refresh_token', refreshToken.value)

            return token.value
        } catch {
            // Si el refresh token ha expirado, cierra la sesión
            cerrarSesion()
            return null
        }
    }

    function cerrarSesion() {
        token.value = null
        refreshToken.value = null
        usuario.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('usuario')
    }

    return {
        token,
        refreshToken,
        usuario,
        estaAutenticado,
        iniciarSesion,
        registrar,
        obtenerPerfil,
        renovarToken,
        cerrarSesion
    }
})