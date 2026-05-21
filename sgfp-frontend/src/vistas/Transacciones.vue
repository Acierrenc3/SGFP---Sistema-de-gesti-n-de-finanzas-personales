<!-- Vista de transacciones con estilo Glassmorphism -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8 animar-lateral">
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
      <div class="glass p-4 mb-4 animar-entrada">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
          <select
            v-model="filtros.tipo"
            @change="aplicarFiltros"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option value="" class="bg-gray-900">Todos los tipos</option>
            <option value="ingreso" class="bg-gray-900">Ingreso</option>
            <option value="gasto" class="bg-gray-900">Gasto</option>
          </select>

          <select
            v-model="filtros.id_categoria"
            @change="aplicarFiltros"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option value="" class="bg-gray-900">Todas las categorías</option>
            <option v-for="cat in categorias" :key="cat.id" :value="cat.id" class="bg-gray-900">
              {{ cat.nombre }}
            </option>
          </select>

          <!-- Búsqueda por descripción -->
          <div class="relative">
            <i class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave text-sm" />
            <input
              v-model="filtros.descripcion"
              type="text"
              placeholder="Buscar por descripción..."
              @input="aplicarFiltros"
              class="w-full pl-9 pr-4 py-2 rounded-xl text-white text-sm placeholder-white/40 outline-none"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <input
            v-model="filtros.fecha_inicio"
            type="date"
            @change="aplicarFiltros"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color-scheme: dark"
          />
          <input
            v-model="filtros.fecha_fin"
            type="date"
            @change="aplicarFiltros"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color-scheme: dark"
          />
        </div>
      </div>

      <!-- Tabla desktop / Tarjetas móvil -->
      <div class="glass overflow-hidden animar-entrada">
        <!-- Cabecera tabla (solo desktop) -->
        <div class="hidden md:grid grid-cols-5 px-6 py-3 text-xs font-medium texto-glass-suave uppercase tracking-wider"
          style="border-bottom: 1px solid rgba(255,255,255,0.08)">
          <span>Fecha</span>
          <span>Tipo</span>
          <span>Descripción</span>
          <span>Categoría</span>
          <span class="text-right">Importe</span>
        </div>

        <!-- Cargando -->
        <div v-if="cargando" class="flex justify-center py-12">
          <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
        </div>

        <!-- Sin datos -->
        <div v-else-if="transacciones.length === 0" class="flex flex-col items-center py-12 texto-glass-suave">
          <i class="pi pi-inbox text-4xl mb-2 opacity-30" />
          <p class="text-sm">No hay transacciones registradas</p>
        </div>

        <template v-else>
          <!-- Vista desktop -->
          <div
            v-for="transaccion in transacciones"
            :key="transaccion.id"
            class="hidden md:grid grid-cols-5 px-6 py-4 items-center transition-all hover:bg-white/5 group animar-entrada"
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

          <!-- Vista móvil (tarjetas) -->
          <div
            v-for="transaccion in transacciones"
            :key="`movil-${transaccion.id}`"
            class="md:hidden flex items-center justify-between px-4 py-3 animar-entrada"
            style="border-bottom: 1px solid rgba(255,255,255,0.05)"
          >
            <div class="flex items-center gap-3">
              <div
                class="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
                :style="transaccion.tipo === 'ingreso'
                  ? 'background: rgba(74,222,128,0.15)'
                  : 'background: rgba(248,113,113,0.15)'"
              >
                <i
                  :class="transaccion.tipo === 'ingreso' ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"
                  :style="transaccion.tipo === 'ingreso' ? 'color: #4ade80' : 'color: #f87171'"
                />
              </div>
              <div>
                <p class="texto-glass text-sm font-medium">
                  {{ transaccion.descripcion || obtenerNombreCategoria(transaccion.id_categoria) }}
                </p>
                <p class="texto-glass-suave text-xs">
                  {{ obtenerNombreCategoria(transaccion.id_categoria) }} · {{ formatearFecha(transaccion.fecha) }}
                </p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span
                class="font-bold text-sm"
                :class="transaccion.tipo === 'ingreso' ? 'text-green-400' : 'text-red-400'"
              >
                {{ transaccion.tipo === 'ingreso' ? '+' : '-' }}{{ formatearMoneda(transaccion.importe) }}
              </span>
              <div class="flex gap-1">
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
        </template>
      </div>

      <!-- Paginación -->
      <div
        v-if="totalPaginas > 1"
        class="flex items-center justify-between px-6 py-4 mt-1 glass"
      >
        <p class="texto-glass-suave text-sm">
          {{ total }} transacciones · Página {{ paginaActual }} de {{ totalPaginas }}
        </p>
        <div class="flex items-center gap-2">
          <button
            @click="cambiarPagina(paginaActual - 1)"
            :disabled="paginaActual === 1"
            class="w-8 h-8 rounded-lg flex items-center justify-center transition-all disabled:opacity-30"
            style="background: rgba(255,255,255,0.08)"
          >
            <i class="pi pi-chevron-left texto-glass text-sm" />
          </button>

          <button
            v-for="pagina in totalPaginas"
            :key="pagina"
            @click="cambiarPagina(pagina)"
            class="w-8 h-8 rounded-lg flex items-center justify-center text-sm transition-all"
            :style="pagina === paginaActual
              ? 'background: linear-gradient(135deg, #7c3aed, #00b4d8); color: white'
              : 'background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.5)'"
          >
            {{ pagina }}
          </button>

          <button
            @click="cambiarPagina(paginaActual + 1)"
            :disabled="paginaActual === totalPaginas"
            class="w-8 h-8 rounded-lg flex items-center justify-center transition-all disabled:opacity-30"
            style="background: rgba(255,255,255,0.08)"
          >
            <i class="pi pi-chevron-right texto-glass text-sm" />
          </button>
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
        <div class="glass w-full max-w-sm p-6 text-center animar-dialogo">
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

const paginaActual = ref(1)
const limite = ref(10)
const total = ref(0)
const totalPaginas = ref(0)

const tiposTransaccion = [
  { etiqueta: 'Ingreso', valor: 'ingreso' },
  { etiqueta: 'Gasto', valor: 'gasto' }
]

const filtros = ref({
  tipo: '',
  id_categoria: '',
  fecha_inicio: '',
  fecha_fin: '',
  descripcion: ''
})

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
    const params = { pagina: paginaActual.value, limite: limite.value }
    if (filtros.value.tipo) params.tipo = filtros.value.tipo
    if (filtros.value.id_categoria) params.id_categoria = filtros.value.id_categoria
    if (filtros.value.fecha_inicio) params.fecha_inicio = new Date(filtros.value.fecha_inicio).toISOString()
    if (filtros.value.fecha_fin) params.fecha_fin = new Date(filtros.value.fecha_fin).toISOString()
    if (filtros.value.descripcion) params.descripcion = filtros.value.descripcion

    const respuesta = await api.get('/transacciones/', { params })
    transacciones.value = respuesta.data.transacciones
    total.value = respuesta.data.total
    totalPaginas.value = respuesta.data.paginas
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las transacciones', life: 3000 })
  } finally {
    cargando.value = false
  }
}

function cambiarPagina(nuevaPagina) {
  if (nuevaPagina < 1 || nuevaPagina > totalPaginas.value) return
  paginaActual.value = nuevaPagina
  cargarTransacciones()
}

function aplicarFiltros() {
  paginaActual.value = 1
  cargarTransacciones()
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