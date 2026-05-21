<!-- Panel de notificaciones con estilo Glassmorphism -->

<template>
  <div class="relative z-50">
    <!-- Botón campana -->
    <button
      @click="togglePanel"
      class="relative w-9 h-9 rounded-xl flex items-center justify-center transition-all hover:bg-white/10"
      style="border: 1px solid rgba(255,255,255,0.1)"
    >
      <i class="pi pi-bell texto-glass text-lg" />
      <span
        v-if="notificacionesStore.notificaciones.length"
        class="absolute -top-1 -right-1 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold text-white"
        style="background: linear-gradient(135deg, #ef4444, #dc2626)"
      >
        {{ notificacionesStore.notificaciones.length }}
      </span>
    </button>

    <!-- Modal centrado -->
    <Transition
      enter-active-class="transition-all duration-200"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition-all duration-150"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="panelAbierto"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px)"
        @click.self="panelAbierto = false"
      >
        <div
          class="w-full max-w-sm"
          style="background: rgba(26,26,46,0.97); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.12); border-radius: 1rem; box-shadow: 0 8px 32px rgba(0,0,0,0.3)"
        >
          <!-- Cabecera -->
          <div class="flex items-center justify-between px-4 py-3" style="border-bottom: 1px solid rgba(255,255,255,0.08)">
            <p class="texto-glass font-semibold text-sm">Notificaciones</p>
            <div class="flex items-center gap-3">
              <button
                v-if="notificacionesStore.notificaciones.length"
                @click="notificacionesStore.limpiarNotificaciones"
                class="texto-glass-suave text-xs hover:text-white transition-colors"
              >
                Limpiar todo
              </button>
              <button
                @click="panelAbierto = false"
                class="w-7 h-7 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-times text-xs" />
              </button>
            </div>
          </div>

          <!-- Lista de notificaciones -->
          <div class="max-h-96 overflow-y-auto">
            <div
              v-if="notificacionesStore.notificaciones.length === 0"
              class="flex flex-col items-center py-10 texto-glass-suave"
            >
              <i class="pi pi-check-circle text-3xl mb-2 opacity-30" />
              <p class="text-sm">Todo en orden</p>
            </div>

            <div
              v-for="notificacion in notificacionesStore.notificaciones"
              :key="notificacion.id"
              class="flex items-start gap-3 px-4 py-3 transition-all hover:bg-white/5"
              style="border-bottom: 1px solid rgba(255,255,255,0.05)"
            >
              <div
                class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                :style="obtenerEstiloIcono(notificacion.tipo)"
              >
                <i :class="notificacion.icono" class="text-sm" />
              </div>

              <div class="flex-1 min-w-0">
                <p class="texto-glass text-xs font-medium">{{ notificacion.categoria }}</p>
                <p class="texto-glass-suave text-xs mt-0.5 leading-relaxed">{{ notificacion.mensaje }}</p>
                <div class="w-full h-1 rounded-full mt-2" style="background: rgba(255,255,255,0.08)">
                  <div
                    class="h-1 rounded-full transition-all"
                    :style="{
                      width: `${Math.min(notificacion.porcentaje, 100)}%`,
                      background: notificacion.tipo === 'error'
                        ? 'linear-gradient(90deg, #ef4444, #dc2626)'
                        : notificacion.tipo === 'warning'
                        ? 'linear-gradient(90deg, #f59e0b, #d97706)'
                        : 'linear-gradient(90deg, #7c3aed, #00b4d8)'
                    }"
                  />
                </div>
                <p class="texto-glass-suave text-xs mt-1">{{ notificacion.porcentaje.toFixed(0) }}% usado</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useNotificacionesStore } from '../stores/notificaciones'

const notificacionesStore = useNotificacionesStore()
const panelAbierto = ref(false)

function togglePanel() {
  panelAbierto.value = !panelAbierto.value
}

function obtenerEstiloIcono(tipo) {
  if (tipo === 'error') return 'background: rgba(239,68,68,0.15); color: #f87171'
  if (tipo === 'warning') return 'background: rgba(245,158,11,0.15); color: #fbbf24'
  return 'background: rgba(124,58,237,0.15); color: #a78bfa'
}
</script>