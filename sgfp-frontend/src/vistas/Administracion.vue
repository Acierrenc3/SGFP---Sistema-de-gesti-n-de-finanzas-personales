<!-- Vista del panel de administración -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8 animar-lateral">
        <div>
          <h2 class="text-2xl font-bold texto-glass">Panel de Administración</h2>
          <p class="texto-glass-suave text-sm mt-1">Gestión global de la plataforma</p>
        </div>
        <div
          class="flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-medium"
          style="background: rgba(124,58,237,0.2); border: 1px solid rgba(124,58,237,0.4); color: #a78bfa"
        >
          <i class="pi pi-shield" />
          Administrador
        </div>
      </div>

      <!-- Estadísticas globales -->
      <div v-if="cargandoEstadisticas" class="flex justify-center py-12">
        <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <div class="glass p-5 animar-entrada">
          <div class="flex items-center justify-between mb-3">
            <p class="texto-glass-suave text-xs">Total usuarios</p>
            <div class="w-8 h-8 rounded-lg flex items-center justify-center"
              style="background: rgba(124,58,237,0.2)">
              <i class="pi pi-users text-purple-400 text-sm" />
            </div>
          </div>
          <p class="text-2xl font-bold texto-glass">{{ estadisticas?.total_usuarios }}</p>
        </div>

        <div class="glass p-5 animar-entrada">
          <div class="flex items-center justify-between mb-3">
            <p class="texto-glass-suave text-xs">Usuarios activos</p>
            <div class="w-8 h-8 rounded-lg flex items-center justify-center"
              style="background: rgba(74,222,128,0.15)">
              <i class="pi pi-user-plus text-green-400 text-sm" />
            </div>
          </div>
          <p class="text-2xl font-bold text-green-400">{{ estadisticas?.usuarios_activos }}</p>
        </div>

        <div class="glass p-5 animar-entrada">
          <div class="flex items-center justify-between mb-3">
            <p class="texto-glass-suave text-xs">Transacciones</p>
            <div class="w-8 h-8 rounded-lg flex items-center justify-center"
              style="background: rgba(0,180,216,0.15)">
              <i class="pi pi-arrow-right-arrow-left text-cyan-400 text-sm" />
            </div>
          </div>
          <p class="text-2xl font-bold text-cyan-400">{{ estadisticas?.total_transacciones }}</p>
        </div>

        <div class="glass p-5 animar-entrada">
          <div class="flex items-center justify-between mb-3">
            <p class="texto-glass-suave text-xs">Ingresos globales</p>
            <div class="w-8 h-8 rounded-lg flex items-center justify-center"
              style="background: rgba(74,222,128,0.15)">
              <i class="pi pi-arrow-up text-green-400 text-sm" />
            </div>
          </div>
          <p class="text-lg font-bold text-green-400">{{ formatearMoneda(estadisticas?.total_ingresos) }}</p>
        </div>

        <div class="glass p-5 animar-entrada">
          <div class="flex items-center justify-between mb-3">
            <p class="texto-glass-suave text-xs">Gastos globales</p>
            <div class="w-8 h-8 rounded-lg flex items-center justify-center"
              style="background: rgba(248,113,113,0.15)">
              <i class="pi pi-arrow-down text-red-400 text-sm" />
            </div>
          </div>
          <p class="text-lg font-bold text-red-400">{{ formatearMoneda(estadisticas?.total_gastos) }}</p>
        </div>
      </div>

      <!-- Lista de usuarios -->
      <div class="glass overflow-hidden animar-entrada">
        <div class="flex items-center justify-between px-6 py-4"
          style="border-bottom: 1px solid rgba(255,255,255,0.08)">
          <h3 class="texto-glass font-semibold">Usuarios registrados</h3>
          <span class="texto-glass-suave text-xs">{{ usuarios.length }} usuarios</span>
        </div>

        <!-- Cargando -->
        <div v-if="cargandoUsuarios" class="flex justify-center py-12">
          <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
        </div>

        <!-- Sin usuarios -->
        <div v-else-if="usuarios.length === 0" class="flex flex-col items-center py-12 texto-glass-suave">
          <i class="pi pi-users text-4xl mb-2 opacity-30" />
          <p class="text-sm">No hay usuarios registrados</p>
        </div>

        <!-- Tabla desktop -->
        <div v-else>
          <!-- Cabecera tabla desktop -->
          <div class="hidden md:grid grid-cols-6 px-6 py-3 text-xs font-medium texto-glass-suave uppercase tracking-wider"
            style="border-bottom: 1px solid rgba(255,255,255,0.08)">
            <span class="col-span-2">Usuario</span>
            <span>Moneda</span>
            <span>Transacciones</span>
            <span>Estado</span>
            <span class="text-right">Acciones</span>
          </div>

          <!-- Filas desktop -->
          <div
            v-for="usuario in usuarios"
            :key="usuario.id"
            class="hidden md:grid grid-cols-6 px-6 py-4 items-center transition-all hover:bg-white/5 group animar-entrada"
            style="border-bottom: 1px solid rgba(255,255,255,0.05)"
          >
            <!-- Nombre y email -->
            <div class="col-span-2 flex items-center gap-3">
              <div
                class="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-white text-sm flex-shrink-0"
                style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
              >
                {{ usuario.nombre?.charAt(0).toUpperCase() }}
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <p class="texto-glass text-sm font-medium">{{ usuario.nombre }}</p>
                  <span
                    v-if="usuario.es_admin"
                    class="text-xs px-1.5 py-0.5 rounded-lg"
                    style="background: rgba(124,58,237,0.2); color: #a78bfa"
                  >
                    Admin
                  </span>
                </div>
                <p class="texto-glass-suave text-xs">{{ usuario.email }}</p>
              </div>
            </div>

            <!-- Moneda -->
            <span class="texto-glass-suave text-sm">{{ usuario.moneda }}</span>

            <!-- Transacciones -->
            <span class="texto-glass text-sm">{{ usuario.total_transacciones }}</span>

            <!-- Estado -->
            <span>
              <span
                class="px-2 py-1 rounded-lg text-xs font-medium"
                :style="usuario.activo
                  ? 'background: rgba(74,222,128,0.15); color: #4ade80'
                  : 'background: rgba(248,113,113,0.15); color: #f87171'"
              >
                {{ usuario.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </span>

            <!-- Acciones -->
            <div class="flex items-center justify-end gap-2">
              <button
                v-if="!usuario.es_admin"
                @click="toggleActivo(usuario)"
                class="w-7 h-7 rounded-lg flex items-center justify-center transition-colors"
                :style="usuario.activo
                  ? 'background: rgba(245,158,11,0.15); color: #fbbf24'
                  : 'background: rgba(74,222,128,0.15); color: #4ade80'"
                :title="usuario.activo ? 'Desactivar' : 'Activar'"
              >
                <i :class="usuario.activo ? 'pi pi-ban text-xs' : 'pi pi-check text-xs'" />
              </button>
              <button
                v-if="!usuario.es_admin"
                @click="confirmarEliminar(usuario)"
                class="w-7 h-7 rounded-lg flex items-center justify-center text-red-400/50 hover:text-red-400 transition-colors"
                style="background: rgba(255,255,255,0.08)"
                title="Eliminar"
              >
                <i class="pi pi-trash text-xs" />
              </button>
            </div>
          </div>

          <!-- Vista móvil -->
          <div
            v-for="usuario in usuarios"
            :key="`movil-${usuario.id}`"
            class="md:hidden flex items-center justify-between px-4 py-3 animar-entrada"
            style="border-bottom: 1px solid rgba(255,255,255,0.05)"
          >
            <div class="flex items-center gap-3">
              <div
                class="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-white text-sm flex-shrink-0"
                style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
              >
                {{ usuario.nombre?.charAt(0).toUpperCase() }}
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <p class="texto-glass text-sm font-medium">{{ usuario.nombre }}</p>
                  <span
                    v-if="usuario.es_admin"
                    class="text-xs px-1.5 py-0.5 rounded-lg"
                    style="background: rgba(124,58,237,0.2); color: #a78bfa"
                  >
                    Admin
                  </span>
                </div>
                <p class="texto-glass-suave text-xs">{{ usuario.email }}</p>
                <div class="flex items-center gap-2 mt-1">
                  <span
                    class="text-xs px-1.5 py-0.5 rounded-lg"
                    :style="usuario.activo
                      ? 'background: rgba(74,222,128,0.15); color: #4ade80'
                      : 'background: rgba(248,113,113,0.15); color: #f87171'"
                  >
                    {{ usuario.activo ? 'Activo' : 'Inactivo' }}
                  </span>
                  <span class="texto-glass-suave text-xs">{{ usuario.total_transacciones }} transacciones</span>
                </div>
              </div>
            </div>

            <div v-if="!usuario.es_admin" class="flex gap-1">
              <button
                @click="toggleActivo(usuario)"
                class="w-7 h-7 rounded-lg flex items-center justify-center transition-colors"
                :style="usuario.activo
                  ? 'background: rgba(245,158,11,0.15); color: #fbbf24'
                  : 'background: rgba(74,222,128,0.15); color: #4ade80'"
              >
                <i :class="usuario.activo ? 'pi pi-ban text-xs' : 'pi pi-check text-xs'" />
              </button>
              <button
                @click="confirmarEliminar(usuario)"
                class="w-7 h-7 rounded-lg flex items-center justify-center text-red-400/50 hover:text-red-400 transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-trash text-xs" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Diálogo confirmar eliminar -->
      <div
        v-if="dialogoEliminarVisible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px)"
      >
        <div class="glass w-full max-w-sm p-6 text-center animar-dialogo">
          <div class="w-14 h-14 rounded-full flex items-center justify-center mx-auto mb-4"
            style="background: rgba(239,68,68,0.15)">
            <i class="pi pi-exclamation-triangle text-red-400 text-2xl" />
          </div>
          <h3 class="text-lg font-bold texto-glass mb-2">¿Eliminar usuario?</h3>
          <p class="texto-glass-suave text-sm mb-1">
            Vas a eliminar a <strong class="texto-glass">{{ usuarioEliminar?.nombre }}</strong>
          </p>
          <p class="texto-glass-suave text-sm mb-6">Esta acción eliminará todos sus datos y no se puede deshacer.</p>
          <div class="flex gap-3">
            <button
              @click="dialogoEliminarVisible = false"
              class="flex-1 py-2 rounded-xl text-sm font-medium texto-glass-suave transition-all hover:text-white"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1)"
            >
              Cancelar
            </button>
            <button
              @click="eliminarUsuario"
              class="flex-1 py-2 rounded-xl text-sm font-semibold text-white transition-all hover:opacity-90"
              style="background: linear-gradient(135deg, #ef4444, #dc2626)"
            >
              Sí, eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
  </LayoutPrincipal>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useRouter } from 'vue-router'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import { useAutenticacionStore } from '../stores/autenticacion'
import api from '../servicios/api'

const toast = useToast()
const enrutador = useRouter()
const autenticacion = useAutenticacionStore()

const estadisticas = ref(null)
const usuarios = ref([])
const cargandoEstadisticas = ref(false)
const cargandoUsuarios = ref(false)
const dialogoEliminarVisible = ref(false)
const usuarioEliminar = ref(null)

function formatearMoneda(valor) {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR'
  }).format(valor || 0)
}

async function cargarEstadisticas() {
  cargandoEstadisticas.value = true
  try {
    const respuesta = await api.get('/admin/estadisticas')
    estadisticas.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las estadísticas', life: 3000 })
  } finally {
    cargandoEstadisticas.value = false
  }
}

async function cargarUsuarios() {
  cargandoUsuarios.value = true
  try {
    const respuesta = await api.get('/admin/usuarios')
    usuarios.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los usuarios', life: 3000 })
  } finally {
    cargandoUsuarios.value = false
  }
}

async function toggleActivo(usuario) {
  try {
    const respuesta = await api.put(`/admin/usuarios/${usuario.id}/toggle-activo`)
    usuario.activo = respuesta.data.activo
    const accion = usuario.activo ? 'activado' : 'desactivado'
    toast.add({ severity: 'success', summary: 'Actualizado', detail: `Usuario ${accion} correctamente`, life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al actualizar', life: 3000 })
  }
}

function confirmarEliminar(usuario) {
  usuarioEliminar.value = usuario
  dialogoEliminarVisible.value = true
}

async function eliminarUsuario() {
  try {
    await api.delete(`/admin/usuarios/${usuarioEliminar.value.id}`)
    toast.add({ severity: 'success', summary: 'Eliminado', detail: 'Usuario eliminado correctamente', life: 3000 })
    dialogoEliminarVisible.value = false
    await cargarUsuarios()
    await cargarEstadisticas()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al eliminar', life: 3000 })
  }
}

onMounted(async () => {
  // Verifica que el usuario es admin
  if (!autenticacion.usuario?.es_admin) {
    enrutador.push({ name: 'Dashboard' })
    return
  }
  await Promise.all([cargarEstadisticas(), cargarUsuarios()])
})
</script>