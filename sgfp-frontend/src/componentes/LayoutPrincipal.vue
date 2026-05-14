<!-- Layout principal con barra lateral Glassmorphism -->

<template>
  <div class="min-h-screen flex" style="background: var(--gradiente-fondo)">
    <!-- Círculos decorativos de fondo -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-96 h-96 rounded-full opacity-10"
        style="background: radial-gradient(circle, #e040fb, transparent)" />
      <div class="absolute -bottom-40 -left-40 w-96 h-96 rounded-full opacity-10"
        style="background: radial-gradient(circle, #00b4d8, transparent)" />
    </div>

    <!-- Barra lateral -->
    <aside class="w-64 flex flex-col fixed h-full z-20"
      style="background: rgba(255,255,255,0.07); backdrop-filter: blur(12px); border-right: 1px solid rgba(255,255,255,0.1)">
      <!-- Logo -->
      <div class="p-6 mb-2" style="border-bottom: 1px solid rgba(255,255,255,0.1)">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center"
            style="background: linear-gradient(135deg, #7c3aed, #00b4d8)">
            <i class="pi pi-wallet text-white text-lg" />
          </div>
          <div>
            <h1 class="text-xl font-bold texto-glass">SGFP</h1>
            <p class="text-xs texto-glass-suave">Finanzas Personales</p>
          </div>
        </div>
      </div>

      <!-- Menú de navegación -->
      <nav class="flex-1 p-4 overflow-y-auto">
        <ul class="flex flex-col gap-1">
          <li v-for="item in menuItems" :key="item.ruta">
            <RouterLink
              :to="item.ruta"
              class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all texto-glass-suave hover:texto-glass group"
              :class="esRutaActiva(item.ruta)
                ? 'text-white font-medium'
                : 'hover:bg-white/10'"
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

      <!-- Información del usuario -->
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

        <!-- Botón cerrar sesión -->
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
    <main class="flex-1 ml-64 relative z-10 overflow-auto min-h-screen">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAutenticacionStore } from '../stores/autenticacion'

const ruta = useRoute()
const enrutador = useRouter()
const toast = useToast()
const autenticacion = useAutenticacionStore()

const menuItems = [
  { etiqueta: 'Dashboard', ruta: '/dashboard', icono: 'pi pi-home' },
  { etiqueta: 'Transacciones', ruta: '/transacciones', icono: 'pi pi-arrow-right-arrow-left' },
  { etiqueta: 'Categorías', ruta: '/categorias', icono: 'pi pi-tag' },
  { etiqueta: 'Presupuestos', ruta: '/presupuestos', icono: 'pi pi-wallet' },
  { etiqueta: 'Cuentas', ruta: '/cuentas', icono: 'pi pi-credit-card' },
  { etiqueta: 'Perfil', ruta: '/perfil', icono: 'pi pi-user' }
]

const inicialUsuario = computed(() => {
  return autenticacion.usuario?.nombre?.charAt(0).toUpperCase() || 'U'
})

function esRutaActiva(rutaItem) {
  return ruta.path === rutaItem
}

function cerrarSesion() {
  autenticacion.cerrarSesion()
  toast.add({ severity: 'info', summary: 'Sesión cerrada', detail: 'Has cerrado sesión correctamente', life: 3000 })
  enrutador.push({ name: 'InicioSesion' })
}
</script>