// Configuración del enrutador de Vue Router
// Basado en: https://router.vuejs.org/guide/

import { createRouter, createWebHistory } from 'vue-router'
import { useAutenticacionStore } from '../stores/autenticacion'

// Importación de vistas
const InicioSesion = () => import('../vistas/InicioSesion.vue')
const Registro = () => import('../vistas/Registro.vue')
const Dashboard = () => import('../vistas/Dashboard.vue')
const Transacciones = () => import('../vistas/Transacciones.vue')
const Categorias = () => import('../vistas/Categorias.vue')
const Presupuestos = () => import('../vistas/Presupuestos.vue')
const Cuentas = () => import('../vistas/Cuentas.vue')
const Perfil = () => import('../vistas/Perfil.vue')

// Definición de rutas
const rutas = [
    {
        path: '/',
        redirect: '/dashboard'
    },
    {
        path: '/inicio-sesion',
        name: 'InicioSesion',
        component: InicioSesion,
        // Solo accesible si no está autenticado
        meta: { requiereInvitado: true }
    },
    {
        path: '/registro',
        name: 'Registro',
        component: Registro,
        meta: { requiereInvitado: true }
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        // Requiere autenticación
        meta: { requiereAuth: true }
    },
    {
        path: '/transacciones',
        name: 'Transacciones',
        component: Transacciones,
        meta: { requiereAuth: true }
    },
    {
        path: '/categorias',
        name: 'Categorias',
        component: Categorias,
        meta: { requiereAuth: true }
    },
    {
        path: '/presupuestos',
        name: 'Presupuestos',
        component: Presupuestos,
        meta: { requiereAuth: true }
    },
    {
        path: '/cuentas',
        name: 'Cuentas',
        component: Cuentas,
        meta: { requiereAuth: true }
    },
    {
        path: '/perfil',
        name: 'Perfil',
        component: Perfil,
        meta: { requiereAuth: true }
    }
]

const enrutador = createRouter({
    // Usa el historial HTML5 sin el símbolo #
    history: createWebHistory(),
    routes: rutas
})

// Guardia de navegación global
// Basado en: https://router.vuejs.org/guide/advanced/navigation-guards.html
enrutador.beforeEach((destino) => {
    const autenticacion = useAutenticacionStore()

    // Redirige al login si la ruta requiere autenticación y no hay sesión
    if (destino.meta.requiereAuth && !autenticacion.estaAutenticado) {
        return { name: 'InicioSesion' }
    }

    // Redirige al dashboard si ya está autenticado e intenta acceder al login
    if (destino.meta.requiereInvitado && autenticacion.estaAutenticado) {
        return { name: 'Dashboard' }
    }
})

export default enrutador