<!-- Layout principal responsive con nav inferior en móvil -->

<template>
  <div class="min-h-screen flex" style="background: var(--gradiente-fondo)">
    <!-- Círculos decorativos -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-96 h-96 rounded-full opacity-10"
        style="background: radial-gradient(circle, #e040fb, transparent)" />
      <div class="absolute -bottom-40 -left-40 w-96 h-96 rounded-full opacity-10"
        style="background: radial-gradient(circle, #00b4d8, transparent)" />
    </div>

    <!-- Barra lateral (solo escritorio) -->
    <aside
      class="hidden md:flex w-64 flex-col fixed h-full z-20"
      style="background: rgba(255,255,255,0.07); backdrop-filter: blur(12px); border-right: 1px solid rgba(255,255,255,0.1)"
    >
      <!-- Logo -->
      <div class="p-6 mb-2" style="border-bottom: 1px solid rgba(255,255,255,0.1)">
        <div class="flex flex-col items-center gap-3 mb-3">
          <img src="/logo.png" alt="SGFP Logo" class="w-24 h-24 rounded-2xl object-cover"
            style="box-shadow: 0 4px 16px rgba(124,58,237,0.3)" />
          <div class="text-center">
            <h1 class="text-xl font-bold texto-glass">SGFP</h1>
            <p class="text-xs texto-glass-suave">Finanzas Personales</p>
          </div>
        </div>
        <div class="flex justify-end">
          <PanelNotificaciones />
        </div>
      </div>

      <!-- Menú navegación -->
      <nav class="flex-1 p-4 overflow-y-auto">
        <ul class="flex flex-col gap-1">
          <li v-for="item in menuItems" :key="item.ruta">
            <RouterLink
              :to="item.ruta"
              class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all texto-glass-suave hover:texto-glass group"
              :class="esRutaActiva(item.ruta) ? 'text-white font-medium' : 'hover:bg-white/10'"
              :style="esRutaActiva(item.ruta)
                ? 'background: linear-gradient(135deg, rgba(124,58,237,0.5), rgba(0,180,216,0.5)); border: 1px solid rgba(255,255,255,0.15)'
                : ''"
            >
              <i :class="item.icono" class="text-lg" />
              <span class="text-sm">{{ item.etiqueta }}</span>
            </RouterLink>
          </li>
        </ul>
      </nav>

      <!-- Usuario y cerrar sesión -->
      <div class="p-4" style="border-top: 1px solid rgba(255,255,255,0.1)">
        <div class="flex items-center gap-3 px-2 py-2 mb-2">
          <div class="w-9 h-9 rounded-full flex items-center justify-center font-bold text-white text-sm flex-shrink-0"
            style="background: linear-gradient(135deg, #7c3aed, #00b4d8)">
            {{ inicialUsuario }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-sm texto-glass truncate">{{ autenticacion.usuario?.nombre }}</p>
            <p class="text-xs texto-glass-suave truncate">{{ autenticacion.usuario?.email }}</p>
          </div>
        </div>
        <button
          @click="cerrarSesion"
          class="w-full flex items-center gap-2 px-4 py-2 rounded-xl text-sm transition-all texto-glass-suave hover:text-red-400 hover:bg-red-400/10"
        >
          <i class="pi pi-sign-out" />
          <span>Cerrar sesión</span>
        </button>
      </div>
    </aside>

    <!-- Contenido principal -->
    <main class="flex-1 md:ml-64 relative z-10 overflow-auto min-h-screen pb-20 md:pb-0">
      <!-- Cabecera móvil -->
      <div
        class="md:hidden flex items-center justify-between px-4 py-3 sticky top-0 z-10"
        style="background: rgba(26,26,46,0.95); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.08)"
      >
        <div class="flex items-center gap-2">
          <img src="/logo.png" alt="SGFP Logo" class="w-8 h-8 rounded-lg object-cover" />
          <span class="font-bold texto-glass">SGFP</span>
        </div>
        <div class="flex items-center gap-3">
          <!-- Notificaciones móvil -->
          <PanelNotificaciones />
          <div class="flex items-center gap-2">
            <span class="texto-glass-suave text-sm hidden sm:block">{{ autenticacion.usuario?.nombre }}</span>
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold"
              style="background: linear-gradient(135deg, #7c3aed, #00b4d8)">
              {{ inicialUsuario }}
            </div>
          </div>
        </div>
        <!-- Diálogo confirmar cerrar sesión -->
        <div
          v-if="dialogoCerrarSesion"
          class="fixed inset-0 z-50 flex items-center justify-center p-4"
          style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px)"
        >
          <div class="glass w-full max-w-sm p-6 text-center">
            <div class="w-14 h-14 rounded-full flex items-center justify-center mx-auto mb-4"
              style="background: rgba(239,68,68,0.15)">
              <i class="pi pi-sign-out text-red-400 text-2xl" />
            </div>
            <h3 class="text-lg font-bold texto-glass mb-2">¿Cerrar sesión?</h3>
            <p class="texto-glass-suave text-sm mb-6">Tu sesión se cerrará y tendrás que volver a iniciar sesión.</p>
            <div class="flex gap-3">
              <button
                @click="dialogoCerrarSesion = false"
                class="flex-1 py-2 rounded-xl text-sm font-medium texto-glass-suave transition-all hover:text-white"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1)"
              >
                Cancelar
              </button>
              <button
                @click="confirmarCerrarSesion"
                class="flex-1 py-2 rounded-xl text-sm font-semibold text-white transition-all hover:opacity-90"
                style="background: linear-gradient(135deg, #ef4444, #dc2626)"
              >
                Sí, cerrar sesión
              </button>
            </div>
          </div>
        </div>
      </div>

      <slot />
    </main>

    <!-- Barra de navegación inferior (solo móvil) -->
    <nav
      class="md:hidden fixed bottom-0 left-0 right-0 z-20 flex items-center justify-around px-2 py-2"
      style="background: rgba(26,26,46,0.97); backdrop-filter: blur(12px); border-top: 1px solid rgba(255,255,255,0.1)"
    >
      <RouterLink
        v-for="item in menuItems"
        :key="item.ruta"
        :to="item.ruta"
        class="flex flex-col items-center gap-1 px-3 py-1 rounded-xl transition-all"
        :style="esRutaActiva(item.ruta)
          ? 'color: #a78bfa'
          : 'color: rgba(255,255,255,0.4)'"
      >
        <i :class="item.icono" class="text-xl" />
        <span class="text-xs">{{ item.etiquetaCorta }}</span>
      </RouterLink>

      <!-- Botón cerrar sesión en móvil -->
      <button
        @click="cerrarSesion"
        class="flex flex-col items-center gap-1 px-3 py-1 rounded-xl transition-all"
        style="color: rgba(255,255,255,0.4)"
      >
        <i class="pi pi-sign-out text-xl" />
        <span class="text-xs">Salir</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAutenticacionStore } from '../stores/autenticacion'
import { useNotificacionesStore } from '../stores/notificaciones'
import PanelNotificaciones from './PanelNotificaciones.vue'

const ruta = useRoute()
const enrutador = useRouter()
const toast = useToast()
const autenticacion = useAutenticacionStore()
const notificacionesStore = useNotificacionesStore()

const menuItems = [
  { etiqueta: 'Dashboard', etiquetaCorta: 'Inicio', ruta: '/dashboard', icono: 'pi pi-home' },
  { etiqueta: 'Transacciones', etiquetaCorta: 'Movimientos', ruta: '/transacciones', icono: 'pi pi-arrow-right-arrow-left' },
  { etiqueta: 'Categorías', etiquetaCorta: 'Categorías', ruta: '/categorias', icono: 'pi pi-tag' },
  { etiqueta: 'Presupuestos', etiquetaCorta: 'Presupuesto', ruta: '/presupuestos', icono: 'pi pi-wallet' },
  { etiqueta: 'Cuentas', etiquetaCorta: 'Cuentas', ruta: '/cuentas', icono: 'pi pi-credit-card' },
  { etiqueta: 'Perfil', etiquetaCorta: 'Perfil', ruta: '/perfil', icono: 'pi pi-user' }
]

const inicialUsuario = computed(() => {
  return autenticacion.usuario?.nombre?.charAt(0).toUpperCase() || 'U'
})

function esRutaActiva(rutaItem) {
  return ruta.path === rutaItem
}

const dialogoCerrarSesion = ref(false)

function cerrarSesion() {
  dialogoCerrarSesion.value = true
}

function confirmarCerrarSesion() {
  dialogoCerrarSesion.value = false
  autenticacion.cerrarSesion()
  toast.add({
    severity: 'info',
    summary: 'Sesión cerrada',
    detail: 'Has cerrado sesión correctamente',
    life: 3000
  })
  enrutador.push({ name: 'InicioSesion' })
}

onMounted(() => {
  notificacionesStore.verificarPresupuestos()
})
</script>