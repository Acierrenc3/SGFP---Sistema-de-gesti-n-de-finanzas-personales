<!-- Layout principal de la aplicación con barra lateral -->
<!-- Basado en: https://primevue.org/drawer/ -->

<template>
  <div class="min-h-screen flex">
    <!-- Barra lateral -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <!-- Logo -->
      <div class="p-6 border-b border-gray-200">
        <h1 class="text-2xl font-bold text-primary-600">SGFP</h1>
        <p class="text-xs text-gray-400 mt-1">Finanzas Personales</p>
      </div>

      <!-- Menú de navegación -->
      <nav class="flex-1 p-4">
        <ul class="flex flex-col gap-1">
          <li v-for="item in menuItems" :key="item.ruta">
            <RouterLink
              :to="item.ruta"
              class="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-primary-50 hover:text-primary-600 transition-colors"
              :class="{ 'bg-primary-50 text-primary-600 font-medium': esRutaActiva(item.ruta) }"
            >
              <i :class="item.icono" class="text-lg" />
              <span>{{ item.etiqueta }}</span>
            </RouterLink>
          </li>
        </ul>
      </nav>

      <!-- Información del usuario -->
      <div class="p-4 border-t border-gray-200">
        <div class="flex items-center gap-3 px-4 py-3">
          <Avatar
            :label="inicialUsuario"
            shape="circle"
            class="bg-primary-100 text-primary-600"
          />
          <div class="flex-1 min-w-0">
            <p class="font-medium text-sm truncate">{{ autenticacion.usuario?.nombre }}</p>
            <p class="text-xs text-gray-400 truncate">{{ autenticacion.usuario?.email }}</p>
          </div>
        </div>

        <!-- Botón cerrar sesión -->
        <Button
          label="Cerrar sesión"
          icon="pi pi-sign-out"
          severity="secondary"
          text
          fluid
          @click="cerrarSesion"
          class="mt-2"
        />
      </div>
    </aside>

    <!-- Contenido principal -->
    <main class="flex-1 bg-gray-50 overflow-auto">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import { useAutenticacionStore } from '../stores/autenticacion'

const ruta = useRoute()
const enrutador = useRouter()
const toast = useToast()
const autenticacion = useAutenticacionStore()

// Elementos del menú de navegación
const menuItems = [
  { etiqueta: 'Dashboard', ruta: '/dashboard', icono: 'pi pi-home' },
  { etiqueta: 'Transacciones', ruta: '/transacciones', icono: 'pi pi-arrow-right-arrow-left' },
  { etiqueta: 'Categorías', ruta: '/categorias', icono: 'pi pi-tag' },
  { etiqueta: 'Presupuestos', ruta: '/presupuestos', icono: 'pi pi-wallet' },
  { etiqueta: 'Cuentas', ruta: '/cuentas', icono: 'pi pi-credit-card' },
  { etiqueta: 'Perfil', ruta: '/perfil', icono: 'pi pi-user' }
]

// Inicial del nombre del usuario para el avatar
const inicialUsuario = computed(() => {
  return autenticacion.usuario?.nombre?.charAt(0).toUpperCase() || 'U'
})

// Comprueba si la ruta actual coincide con la del menú
function esRutaActiva(rutaItem) {
  return ruta.path === rutaItem
}

function cerrarSesion() {
  autenticacion.cerrarSesion()
  toast.add({
    severity: 'info',
    summary: 'Sesión cerrada',
    detail: 'Has cerrado sesión correctamente',
    life: 3000
  })
  enrutador.push({ name: 'InicioSesion' })
}
</script>