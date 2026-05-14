// Store de autenticación con Pinia
// Basado en: https://pinia.vuejs.org/core-concepts/

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../servicios/api'

export const useAutenticacionStore = defineStore('autenticacion', () => {
    // Estado
    const token = ref(localStorage.getItem('token') || null)
    const usuario = ref(JSON.parse(localStorage.getItem('usuario') || 'null'))

    // Computed
    const estaAutenticado = computed(() => !!token.value)

    // Acciones
    async function iniciarSesion(email, contrasena) {
        // OAuth2PasswordRequestForm espera FormData con 'username' y 'password'
        const formulario = new FormData()
        formulario.append('username', email)
        formulario.append('password', contrasena)

        const respuesta = await api.post('/auth/token', formulario)

        // Guarda el token en el estado y en localStorage
        token.value = respuesta.data.access_token
        localStorage.setItem('token', token.value)

        // Obtiene los datos del usuario autenticado
        await obtenerPerfil()
    }

    async function registrar(nombre, email, contrasena) {
        await api.post('/auth/registro', {
            nombre,
            email,
            contrasena
        })
    }

    async function obtenerPerfil() {
        const respuesta = await api.get('/usuarios/perfil')
        usuario.value = respuesta.data
        localStorage.setItem('usuario', JSON.stringify(usuario.value))
    }

    function cerrarSesion() {
        // Limpia el estado y localStorage
        token.value = null
        usuario.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('usuario')
    }

    return {
        token,
        usuario,
        estaAutenticado,
        iniciarSesion,
        registrar,
        obtenerPerfil,
        cerrarSesion
    }
})