// Configuración del enrutador de Vue Router
// Basado en: https://router.vuejs.org/guide/

import { createRouter, createWebHistory } from 'vue-router'
import { useAutenticacionStore } from '../stores/autenticacion'

const LandingPage = () => import('../vistas/LandingPage.vue')
const InicioSesion = () => import('../vistas/InicioSesion.vue')
const Registro = () => import('../vistas/Registro.vue')
const Dashboard = () => import('../vistas/Dashboard.vue')
const Transacciones = () => import('../vistas/Transacciones.vue')
const Categorias = () => import('../vistas/Categorias.vue')
const Presupuestos = () => import('../vistas/Presupuestos.vue')
const Cuentas = () => import('../vistas/Cuentas.vue')
const Perfil = () => import('../vistas/Perfil.vue')
const Recurrentes = () => import('../vistas/Recurrentes.vue')

const rutas = [
    {
        path: '/',
        name: 'LandingPage',
        component: LandingPage,
        meta: { publica: true }
    },
    {
        path: '/inicio-sesion',
        name: 'InicioSesion',
        component: InicioSesion,
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
    },
    {
        path: '/recurrentes',
        name: 'Recurrentes',
        component: Recurrentes,
        meta: { requiereAuth: true }
    }
]

const enrutador = createRouter({
    history: createWebHistory(),
    routes: rutas,
    // Scroll al inicio al cambiar de página
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) return savedPosition
        if (to.hash) return { el: to.hash, behavior: 'smooth' }
        return { top: 0 }
    }
})

enrutador.beforeEach((destino) => {
    const autenticacion = useAutenticacionStore()

    // Si está autenticado y va a la landing → redirige al dashboard
    if (destino.meta.publica && autenticacion.estaAutenticado) {
        return { name: 'Dashboard' }
    }

    // Si requiere auth y no está autenticado → redirige al login
    if (destino.meta.requiereAuth && !autenticacion.estaAutenticado) {
        return { name: 'InicioSesion' }
    }

    // Si requiere ser invitado y está autenticado → redirige al dashboard
    if (destino.meta.requiereInvitado && autenticacion.estaAutenticado) {
        return { name: 'Dashboard' }
    }
})

export default enrutador