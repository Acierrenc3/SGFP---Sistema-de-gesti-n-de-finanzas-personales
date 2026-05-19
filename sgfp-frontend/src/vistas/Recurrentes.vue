<!-- Vista de transacciones recurrentes con estilo Glassmorphism -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8 animar-lateral">
        <div>
          <h2 class="text-2xl font-bold texto-glass">Recurrentes</h2>
          <p class="texto-glass-suave text-sm mt-1">Gestiona tus ingresos y gastos automáticos</p>
        </div>
        <button
          @click="abrirDialogo()"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-white text-sm font-medium transition-all hover:opacity-90 active:scale-95"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <i class="pi pi-plus" />
          Nuevo recurrente
        </button>
      </div>

      <!-- Grid de recurrentes -->
      <div v-if="cargando" class="flex justify-center py-12">
        <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
      </div>

      <div v-else-if="recurrentes.length === 0" class="glass flex flex-col items-center py-12 texto-glass-suave animar-entrada">
        <i class="pi pi-sync text-4xl mb-2 opacity-30" />
        <p class="text-sm mb-1">No hay transacciones recurrentes</p>
        <p class="text-xs opacity-60">Añade ingresos o gastos que se repitan automáticamente</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="recurrente in recurrentes"
          :key="recurrente.id"
          class="glass p-5 group animar-entrada"
          :style="!recurrente.activo ? 'opacity: 0.6' : ''"
        >
          <!-- Cabecera tarjeta -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <!-- Icono tipo -->
              <div
                class="w-10 h-10 rounded-xl flex items-center justify-center"
                :style="recurrente.tipo === 'ingreso'
                  ? 'background: rgba(74,222,128,0.15)'
                  : 'background: rgba(248,113,113,0.15)'"
              >
                <i
                  :class="recurrente.tipo === 'ingreso' ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"
                  :style="recurrente.tipo === 'ingreso' ? 'color: #4ade80' : 'color: #f87171'"
                />
              </div>
              <div>
                <p class="texto-glass font-medium text-sm">{{ recurrente.descripcion }}</p>
                <p class="texto-glass-suave text-xs">{{ obtenerNombreCategoria(recurrente.id_categoria) }}</p>
              </div>
            </div>

            <!-- Acciones -->
            <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                @click="togglePausar(recurrente)"
                class="w-7 h-7 rounded-lg flex items-center justify-center transition-colors"
                :style="recurrente.activo
                  ? 'background: rgba(245,158,11,0.15); color: #fbbf24'
                  : 'background: rgba(74,222,128,0.15); color: #4ade80'"
                :title="recurrente.activo ? 'Pausar' : 'Reanudar'"
              >
                <i :class="recurrente.activo ? 'pi pi-pause text-xs' : 'pi pi-play text-xs'" />
              </button>
              <button
                @click="abrirDialogo(recurrente)"
                class="w-7 h-7 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-pencil text-xs" />
              </button>
              <button
                @click="confirmarEliminar(recurrente)"
                class="w-7 h-7 rounded-lg flex items-center justify-center text-red-400/50 hover:text-red-400 transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-trash text-xs" />
              </button>
            </div>
          </div>

          <!-- Importe -->
          <p
            class="text-2xl font-bold mb-3"
            :class="recurrente.tipo === 'ingreso' ? 'text-green-400' : 'text-red-400'"
          >
            {{ recurrente.tipo === 'ingreso' ? '+' : '-' }}{{ formatearMoneda(recurrente.importe) }}
          </p>

          <!-- Info -->
          <div style="border-top: 1px solid rgba(255,255,255,0.08)" class="pt-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <i class="pi pi-sync texto-glass-suave text-xs" />
                <span class="texto-glass-suave text-xs">{{ obtenerEtiquetaFrecuencia(recurrente.frecuencia) }}</span>
              </div>
              <!-- Badge activo/pausado -->
              <span
                class="text-xs px-2 py-0.5 rounded-lg"
                :style="recurrente.activo
                  ? 'background: rgba(74,222,128,0.15); color: #4ade80'
                  : 'background: rgba(245,158,11,0.15); color: #fbbf24'"
              >
                {{ recurrente.activo ? 'Activo' : 'Pausado' }}
              </span>
            </div>
            <div class="flex items-center gap-2 mt-2">
              <i class="pi pi-calendar texto-glass-suave text-xs" />
              <span class="texto-glass-suave text-xs">
                Próxima: {{ formatearFecha(recurrente.proxima_ejecucion) }}
              </span>
            </div>
            <div v-if="recurrente.fecha_fin" class="flex items-center gap-2 mt-1">
              <i class="pi pi-calendar-times texto-glass-suave text-xs" />
              <span class="texto-glass-suave text-xs">
                Fin: {{ formatearFecha(recurrente.fecha_fin) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Diálogo crear/editar -->
      <div
        v-if="dialogoVisible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px)"
        @click.self="dialogoVisible = false"
      >
        <div class="glass w-full max-w-lg p-6 animar-dialogo overflow-y-auto max-h-screen">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold texto-glass">
              {{ recurrenteEditando ? 'Editar recurrente' : 'Nuevo recurrente' }}
            </h3>
            <button
              @click="dialogoVisible = false"
              class="w-8 h-8 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
              style="background: rgba(255,255,255,0.08)"
            >
              <i class="pi pi-times text-sm" />
            </button>
          </div>

          <form @submit.prevent="guardarRecurrente" class="flex flex-col gap-4">
            <!-- Tipo -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Tipo</label>
              <div class="flex gap-2">
                <button
                  type="button"
                  v-for="tipo in tiposTransaccion"
                  :key="tipo.valor"
                  @click="formulario.tipo = tipo.valor"
                  class="flex-1 py-2 rounded-xl text-sm font-medium transition-all"
                  :style="formulario.tipo === tipo.valor
                    ? tipo.valor === 'ingreso'
                      ? 'background: rgba(74,222,128,0.2); color: #4ade80; border: 1px solid rgba(74,222,128,0.4)'
                      : 'background: rgba(248,113,113,0.2); color: #f87171; border: 1px solid rgba(248,113,113,0.4)'
                    : 'background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.1)'"
                >
                  {{ tipo.etiqueta }}
                </button>
              </div>
            </div>

            <!-- Descripción -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Descripción</label>
              <input
                v-model="formulario.descripcion"
                type="text"
                placeholder="Ej: Sueldo mensual, Netflix, Alquiler..."
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.descripcion ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="text-red-400" v-if="errores.descripcion">{{ errores.descripcion }}</small>
            </div>

            <!-- Importe -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Importe</label>
              <input
                v-model="formulario.importe"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.importe ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="text-red-400" v-if="errores.importe">{{ errores.importe }}</small>
            </div>

            <!-- Frecuencia -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Frecuencia</label>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                <button
                  type="button"
                  v-for="freq in frecuencias"
                  :key="freq.valor"
                  @click="formulario.frecuencia = freq.valor"
                  class="py-2 rounded-xl text-sm font-medium transition-all"
                  :style="formulario.frecuencia === freq.valor
                    ? 'background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(0,180,216,0.4)); color: white; border: 1px solid rgba(124,58,237,0.5)'
                    : 'background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.1)'"
                >
                  {{ freq.etiqueta }}
                </button>
              </div>
            </div>

            <!-- Día de repetición (solo mensual) -->
            <div class="flex flex-col gap-2" v-if="formulario.frecuencia === 'mensual'">
              <label class="texto-glass text-sm font-medium">Día del mes (1-28)</label>
              <input
                v-model="formulario.dia_repeticion"
                type="number"
                min="1"
                max="28"
                placeholder="Ej: 1, 5, 15, 28..."
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
              />
            </div>

            <!-- Categoría -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Categoría</label>
              <select
                v-model="formulario.id_categoria"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.id_categoria ? 'border-red-400' : 'focus:border-purple-400'"
              >
                <option value="" class="bg-gray-900">Selecciona una categoría</option>
                <option v-for="cat in categoriasFiltradas" :key="cat.id" :value="cat.id" class="bg-gray-900">
                  {{ cat.nombre }}
                </option>
              </select>
              <small class="text-red-400" v-if="errores.id_categoria">{{ errores.id_categoria }}</small>
            </div>

            <!-- Cuenta -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Cuenta</label>
              <select
                v-model="formulario.id_cuenta"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.id_cuenta ? 'border-red-400' : 'focus:border-purple-400'"
              >
                <option value="" class="bg-gray-900">Selecciona una cuenta</option>
                <option v-for="cuenta in cuentas" :key="cuenta.id" :value="cuenta.id" class="bg-gray-900">
                  {{ cuenta.nombre }}
                </option>
              </select>
              <small class="text-red-400" v-if="errores.id_cuenta">{{ errores.id_cuenta }}</small>
            </div>

            <!-- Fecha inicio -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Fecha de inicio</label>
              <input
                v-model="formulario.fecha_inicio"
                type="date"
                class="w-full px-4 py-3 rounded-xl text-white outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color-scheme: dark"
                :class="errores.fecha_inicio ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="text-red-400" v-if="errores.fecha_inicio">{{ errores.fecha_inicio }}</small>
            </div>

            <!-- Fecha fin (opcional) -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Fecha de fin (opcional)</label>
              <input
                v-model="formulario.fecha_fin"
                type="date"
                class="w-full px-4 py-3 rounded-xl text-white outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color-scheme: dark"
              />
              <small class="texto-glass-suave text-xs">Deja vacío para que se repita indefinidamente</small>
            </div>

            <!-- Botones -->
            <div class="flex gap-3 mt-2">
              <button
                type="button"
                @click="dialogoVisible = false"
                class="flex-1 py-3 rounded-xl text-sm font-medium texto-glass-suave transition-all hover:text-white"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1)"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="guardando"
                class="flex-1 py-3 rounded-xl text-sm font-semibold text-white transition-all hover:opacity-90 disabled:opacity-50"
                style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
              >
                <span v-if="!guardando">{{ recurrenteEditando ? 'Guardar cambios' : 'Crear recurrente' }}</span>
                <i v-else class="pi pi-spin pi-spinner" />
              </button>
            </div>
          </form>
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
          <h3 class="text-lg font-bold texto-glass mb-2">¿Eliminar recurrente?</h3>
          <p class="texto-glass-suave text-sm mb-6">Esta acción no se puede deshacer.</p>
          <div class="flex gap-3">
            <button
              @click="dialogoEliminarVisible = false"
              class="flex-1 py-2 rounded-xl text-sm font-medium texto-glass-suave transition-all hover:text-white"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1)"
            >
              Cancelar
            </button>
            <button
              @click="eliminarRecurrente"
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
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import { useAutenticacionStore } from '../stores/autenticacion'
import api from '../servicios/api'

const toast = useToast()
const autenticacion = useAutenticacionStore()

const recurrentes = ref([])
const categorias = ref([])
const cuentas = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const dialogoEliminarVisible = ref(false)
const recurrenteEditando = ref(null)
const recurrenteEliminar = ref(null)
const errores = ref({})

const tiposTransaccion = [
  { etiqueta: 'Ingreso', valor: 'ingreso' },
  { etiqueta: 'Gasto', valor: 'gasto' }
]

const frecuencias = [
  { etiqueta: 'Diario', valor: 'diario' },
  { etiqueta: 'Semanal', valor: 'semanal' },
  { etiqueta: 'Mensual', valor: 'mensual' },
  { etiqueta: 'Anual', valor: 'anual' }
]

const formulario = ref({
  tipo: 'gasto',
  descripcion: '',
  importe: '',
  frecuencia: 'mensual',
  dia_repeticion: null,
  fecha_inicio: new Date().toISOString().split('T')[0],
  fecha_fin: '',
  id_categoria: '',
  id_cuenta: ''
})

const categoriasFiltradas = computed(() => {
  return categorias.value.filter(c => c.tipo === formulario.value.tipo)
})

function obtenerNombreCategoria(id) {
  return categorias.value.find(c => c.id === id)?.nombre || '-'
}

function obtenerEtiquetaFrecuencia(frecuencia) {
  return frecuencias.find(f => f.valor === frecuencia)?.etiqueta || frecuencia
}

function formatearFecha(fecha) {
  return new Date(fecha).toLocaleDateString('es-ES')
}

function formatearMoneda(valor) {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: autenticacion.usuario?.moneda || 'EUR'
  }).format(valor)
}

async function cargarRecurrentes() {
  cargando.value = true
  try {
    const respuesta = await api.get('/recurrentes/')
    recurrentes.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los recurrentes', life: 3000 })
  } finally {
    cargando.value = false
  }
}

async function cargarCategorias() {
  const respuesta = await api.get('/categorias/')
  categorias.value = respuesta.data
}

async function cargarCuentas() {
  const respuesta = await api.get('/cuentas/')
  cuentas.value = respuesta.data
}

function abrirDialogo(recurrente = null) {
  errores.value = {}
  recurrenteEditando.value = recurrente

  if (recurrente) {
    formulario.value = {
      tipo: recurrente.tipo,
      descripcion: recurrente.descripcion,
      importe: recurrente.importe,
      frecuencia: recurrente.frecuencia,
      dia_repeticion: recurrente.dia_repeticion,
      fecha_inicio: recurrente.fecha_inicio.split('T')[0],
      fecha_fin: recurrente.fecha_fin ? recurrente.fecha_fin.split('T')[0] : '',
      id_categoria: recurrente.id_categoria,
      id_cuenta: recurrente.id_cuenta
    }
  } else {
    formulario.value = {
      tipo: 'gasto',
      descripcion: '',
      importe: '',
      frecuencia: 'mensual',
      dia_repeticion: null,
      fecha_inicio: new Date().toISOString().split('T')[0],
      fecha_fin: '',
      id_categoria: '',
      id_cuenta: ''
    }
  }

  dialogoVisible.value = true
}

function validar() {
  errores.value = {}
  if (!formulario.value.descripcion) errores.value.descripcion = 'La descripción es obligatoria'
  if (!formulario.value.importe) errores.value.importe = 'El importe es obligatorio'
  if (!formulario.value.id_categoria) errores.value.id_categoria = 'La categoría es obligatoria'
  if (!formulario.value.id_cuenta) errores.value.id_cuenta = 'La cuenta es obligatoria'
  if (!formulario.value.fecha_inicio) errores.value.fecha_inicio = 'La fecha de inicio es obligatoria'
  return Object.keys(errores.value).length === 0
}

async function guardarRecurrente() {
  if (!validar()) return
  guardando.value = true

  try {
    const datos = {
      ...formulario.value,
      importe: parseFloat(formulario.value.importe),
      fecha_inicio: new Date(formulario.value.fecha_inicio).toISOString(),
      fecha_fin: formulario.value.fecha_fin
        ? new Date(formulario.value.fecha_fin).toISOString()
        : null,
      dia_repeticion: formulario.value.dia_repeticion
        ? parseInt(formulario.value.dia_repeticion)
        : null
    }

    if (recurrenteEditando.value) {
      await api.put(`/recurrentes/${recurrenteEditando.value.id}`, datos)
      toast.add({ severity: 'success', summary: 'Actualizado', detail: 'Recurrente actualizado correctamente', life: 3000 })
    } else {
      await api.post('/recurrentes/', datos)
      toast.add({ severity: 'success', summary: 'Creado', detail: 'Recurrente creado correctamente', life: 3000 })
    }

    dialogoVisible.value = false
    await cargarRecurrentes()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al guardar', life: 3000 })
  } finally {
    guardando.value = false
  }
}

async function togglePausar(recurrente) {
  try {
    await api.post(`/recurrentes/${recurrente.id}/pausar`)
    const accion = recurrente.activo ? 'pausado' : 'reanudado'
    toast.add({ severity: 'success', summary: 'Actualizado', detail: `Recurrente ${accion} correctamente`, life: 3000 })
    await cargarRecurrentes()
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo actualizar el recurrente', life: 3000 })
  }
}

function confirmarEliminar(recurrente) {
  recurrenteEliminar.value = recurrente
  dialogoEliminarVisible.value = true
}

async function eliminarRecurrente() {
  try {
    await api.delete(`/recurrentes/${recurrenteEliminar.value.id}`)
    toast.add({ severity: 'success', summary: 'Eliminado', detail: 'Recurrente eliminado correctamente', life: 3000 })
    dialogoEliminarVisible.value = false
    await cargarRecurrentes()
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar el recurrente', life: 3000 })
  }
}

onMounted(async () => {
  await Promise.all([cargarRecurrentes(), cargarCategorias(), cargarCuentas()])
})
</script>