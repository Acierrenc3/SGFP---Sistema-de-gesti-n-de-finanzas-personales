<!-- Vista de transacciones con estilo Glassmorphism -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-2xl font-bold texto-glass">Transacciones</h2>
          <p class="texto-glass-suave text-sm mt-1">Gestiona tus ingresos y gastos</p>
        </div>
        <button
          @click="abrirDialogo()"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-white text-sm font-medium transition-all hover:opacity-90 active:scale-95"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <i class="pi pi-plus" />
          Nueva transacción
        </button>
      </div>

      <!-- Filtros -->
      <div class="glass p-4 mb-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
          <select
            v-model="filtros.tipo"
            @change="cargarTransacciones"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option value="" class="bg-gray-900">Todos los tipos</option>
            <option value="ingreso" class="bg-gray-900">Ingreso</option>
            <option value="gasto" class="bg-gray-900">Gasto</option>
          </select>

          <select
            v-model="filtros.id_categoria"
            @change="cargarTransacciones"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option value="" class="bg-gray-900">Todas las categorías</option>
            <option v-for="cat in categorias" :key="cat.id" :value="cat.id" class="bg-gray-900">
              {{ cat.nombre }}
            </option>
          </select>

          <input
            v-model="filtros.fecha_inicio"
            type="date"
            @change="cargarTransacciones"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color-scheme: dark"
          />

          <input
            v-model="filtros.fecha_fin"
            type="date"
            @change="cargarTransacciones"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color-scheme: dark"
          />
        </div>
      </div>

      <!-- Tabla de transacciones -->
      <div class="glass overflow-hidden">
        <!-- Cabecera tabla -->
        <div class="grid grid-cols-5 px-6 py-3 text-xs font-medium texto-glass-suave uppercase tracking-wider"
          style="border-bottom: 1px solid rgba(255,255,255,0.08)">
          <span>Fecha</span>
          <span>Tipo</span>
          <span>Descripción</span>
          <span>Categoría</span>
          <span class="text-right">Importe</span>
        </div>

        <!-- Filas -->
        <div v-if="cargando" class="flex justify-center py-12">
          <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
        </div>

        <div v-else-if="transacciones.length === 0" class="flex flex-col items-center py-12 texto-glass-suave">
          <i class="pi pi-inbox text-4xl mb-2 opacity-30" />
          <p class="text-sm">No hay transacciones registradas</p>
        </div>

        <div
          v-else
          v-for="transaccion in transacciones"
          :key="transaccion.id"
          class="grid grid-cols-5 px-6 py-4 items-center transition-all hover:bg-white/5 group"
          style="border-bottom: 1px solid rgba(255,255,255,0.05)"
        >
          <span class="texto-glass text-sm">{{ formatearFecha(transaccion.fecha) }}</span>

          <span>
            <span
              class="px-2 py-1 rounded-lg text-xs font-medium"
              :style="transaccion.tipo === 'ingreso'
                ? 'background: rgba(74,222,128,0.15); color: #4ade80'
                : 'background: rgba(248,113,113,0.15); color: #f87171'"
            >
              {{ transaccion.tipo === 'ingreso' ? 'Ingreso' : 'Gasto' }}
            </span>
          </span>

          <span class="texto-glass text-sm truncate">{{ transaccion.descripcion || '-' }}</span>

          <span class="texto-glass-suave text-sm">{{ obtenerNombreCategoria(transaccion.id_categoria) }}</span>

          <div class="flex items-center justify-end gap-3">
            <span
              class="font-bold text-sm"
              :class="transaccion.tipo === 'ingreso' ? 'text-green-400' : 'text-red-400'"
            >
              {{ transaccion.tipo === 'ingreso' ? '+' : '-' }}{{ formatearMoneda(transaccion.importe) }}
            </span>
            <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                @click="abrirDialogo(transaccion)"
                class="w-7 h-7 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-pencil text-xs" />
              </button>
              <button
                @click="confirmarEliminar(transaccion)"
                class="w-7 h-7 rounded-lg flex items-center justify-center text-red-400/50 hover:text-red-400 transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-trash text-xs" />
              </button>
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
        <div class="glass w-full max-w-lg p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold texto-glass">
              {{ transaccionEditando ? 'Editar transacción' : 'Nueva transacción' }}
            </h3>
            <button
              @click="dialogoVisible = false"
              class="w-8 h-8 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
              style="background: rgba(255,255,255,0.08)"
            >
              <i class="pi pi-times text-sm" />
            </button>
          </div>

          <form @submit.prevent="guardarTransaccion" class="flex flex-col gap-4">
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

            <!-- Fecha -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Fecha</label>
              <input
                v-model="formulario.fecha"
                type="date"
                class="w-full px-4 py-3 rounded-xl text-white outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color-scheme: dark"
                :class="errores.fecha ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="text-red-400" v-if="errores.fecha">{{ errores.fecha }}</small>
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

            <!-- Descripción -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Descripción (opcional)</label>
              <textarea
                v-model="formulario.descripcion"
                rows="2"
                placeholder="Descripción de la transacción"
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all resize-none"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
              />
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
                <span v-if="!guardando">{{ transaccionEditando ? 'Guardar cambios' : 'Crear transacción' }}</span>
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
        <div class="glass w-full max-w-sm p-6 text-center">
          <div class="w-14 h-14 rounded-full flex items-center justify-center mx-auto mb-4"
            style="background: rgba(239,68,68,0.15)">
            <i class="pi pi-exclamation-triangle text-red-400 text-2xl" />
          </div>
          <h3 class="text-lg font-bold texto-glass mb-2">¿Eliminar transacción?</h3>
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
              @click="eliminarTransaccion"
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

const transacciones = ref([])
const categorias = ref([])
const cuentas = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const dialogoEliminarVisible = ref(false)
const transaccionEditando = ref(null)
const transaccionEliminar = ref(null)
const errores = ref({})

const tiposTransaccion = [
  { etiqueta: 'Ingreso', valor: 'ingreso' },
  { etiqueta: 'Gasto', valor: 'gasto' }
]

const filtros = ref({ tipo: '', id_categoria: '', fecha_inicio: '', fecha_fin: '' })

const formulario = ref({
  tipo: 'gasto',
  importe: '',
  fecha: new Date().toISOString().split('T')[0],
  descripcion: '',
  id_categoria: '',
  id_cuenta: ''
})

const categoriasFiltradas = computed(() => {
  return categorias.value.filter(c => c.tipo === formulario.value.tipo)
})

function obtenerNombreCategoria(id) {
  return categorias.value.find(c => c.id === id)?.nombre || '-'
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

async function cargarTransacciones() {
  cargando.value = true
  try {
    const params = {}
    if (filtros.value.tipo) params.tipo = filtros.value.tipo
    if (filtros.value.id_categoria) params.id_categoria = filtros.value.id_categoria
    if (filtros.value.fecha_inicio) params.fecha_inicio = new Date(filtros.value.fecha_inicio).toISOString()
    if (filtros.value.fecha_fin) params.fecha_fin = new Date(filtros.value.fecha_fin).toISOString()
    const respuesta = await api.get('/transacciones/', { params })
    transacciones.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las transacciones', life: 3000 })
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

function abrirDialogo(transaccion = null) {
  errores.value = {}
  transaccionEditando.value = transaccion
  if (transaccion) {
    formulario.value = {
      tipo: transaccion.tipo,
      importe: transaccion.importe,
      fecha: transaccion.fecha.split('T')[0],
      descripcion: transaccion.descripcion || '',
      id_categoria: transaccion.id_categoria,
      id_cuenta: transaccion.id_cuenta
    }
  } else {
    formulario.value = {
      tipo: 'gasto',
      importe: '',
      fecha: new Date().toISOString().split('T')[0],
      descripcion: '',
      id_categoria: '',
      id_cuenta: ''
    }
  }
  dialogoVisible.value = true
}

function validar() {
  errores.value = {}
  if (!formulario.value.importe) errores.value.importe = 'El importe es obligatorio'
  if (!formulario.value.fecha) errores.value.fecha = 'La fecha es obligatoria'
  if (!formulario.value.id_categoria) errores.value.id_categoria = 'La categoría es obligatoria'
  if (!formulario.value.id_cuenta) errores.value.id_cuenta = 'La cuenta es obligatoria'
  return Object.keys(errores.value).length === 0
}

async function guardarTransaccion() {
  if (!validar()) return
  guardando.value = true
  try {
    const datos = {
      ...formulario.value,
      importe: parseFloat(formulario.value.importe),
      fecha: new Date(formulario.value.fecha).toISOString()
    }
    if (transaccionEditando.value) {
      await api.put(`/transacciones/${transaccionEditando.value.id}`, datos)
      toast.add({ severity: 'success', summary: 'Actualizada', detail: 'Transacción actualizada correctamente', life: 3000 })
    } else {
      await api.post('/transacciones/', datos)
      toast.add({ severity: 'success', summary: 'Creada', detail: 'Transacción creada correctamente', life: 3000 })
    }
    dialogoVisible.value = false
    await cargarTransacciones()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al guardar', life: 3000 })
  } finally {
    guardando.value = false
  }
}

function confirmarEliminar(transaccion) {
  transaccionEliminar.value = transaccion
  dialogoEliminarVisible.value = true
}

async function eliminarTransaccion() {
  try {
    await api.delete(`/transacciones/${transaccionEliminar.value.id}`)
    toast.add({ severity: 'success', summary: 'Eliminada', detail: 'Transacción eliminada correctamente', life: 3000 })
    dialogoEliminarVisible.value = false
    await cargarTransacciones()
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar la transacción', life: 3000 })
  }
}

onMounted(async () => {
  await Promise.all([cargarTransacciones(), cargarCategorias(), cargarCuentas()])
})
</script>