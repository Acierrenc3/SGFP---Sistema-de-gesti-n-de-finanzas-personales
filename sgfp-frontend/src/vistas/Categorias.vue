<!-- Vista de presupuestos con estilo Glassmorphism -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-2xl font-bold texto-glass">Presupuestos</h2>
          <p class="texto-glass-suave text-sm mt-1">Gestiona tus límites de gasto mensuales</p>
        </div>
        <button
          @click="abrirDialogo()"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-white text-sm font-medium transition-all hover:opacity-90 active:scale-95"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <i class="pi pi-plus" />
          Nuevo presupuesto
        </button>
      </div>

      <!-- Filtros -->
      <div class="glass p-4 mb-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <select
            v-model="filtros.mes"
            @change="cargarPresupuestos"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option value="" class="bg-gray-900">Todos los meses</option>
            <option v-for="mes in meses" :key="mes.valor" :value="mes.valor" class="bg-gray-900">
              {{ mes.etiqueta }}
            </option>
          </select>
          <select
            v-model="filtros.anio"
            @change="cargarPresupuestos"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option value="" class="bg-gray-900">Todos los años</option>
            <option v-for="anio in anios" :key="anio" :value="anio" class="bg-gray-900">
              {{ anio }}
            </option>
          </select>
        </div>
      </div>

      <!-- Grid de presupuestos -->
      <div v-if="cargando" class="flex justify-center py-12">
        <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
      </div>

      <div v-else-if="presupuestos.length === 0" class="glass flex flex-col items-center py-12 texto-glass-suave">
        <i class="pi pi-wallet text-4xl mb-2 opacity-30" />
        <p class="text-sm">No hay presupuestos registrados</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="presupuesto in presupuestos"
          :key="presupuesto.id"
          class="glass p-5 group"
        >
          <!-- Cabecera tarjeta -->
          <div class="flex items-center justify-between mb-4">
            <div>
              <p class="texto-glass font-medium text-sm">{{ obtenerNombreCategoria(presupuesto.id_categoria) }}</p>
              <p class="texto-glass-suave text-xs mt-0.5">
                {{ obtenerNombreMes(presupuesto.mes) }} {{ presupuesto.anio }}
              </p>
            </div>
            <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                @click="abrirDialogo(presupuesto)"
                class="w-7 h-7 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-pencil text-xs" />
              </button>
              <button
                @click="confirmarEliminar(presupuesto)"
                class="w-7 h-7 rounded-lg flex items-center justify-center text-red-400/50 hover:text-red-400 transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-trash text-xs" />
              </button>
            </div>
          </div>

          <!-- Importe límite -->
          <p class="text-2xl font-bold texto-glass mb-3">
            {{ formatearMoneda(presupuesto.importe_limite) }}
          </p>

          <!-- Barra de progreso (estática, sin dato real aquí) -->
          <div class="w-full h-1.5 rounded-full" style="background: rgba(255,255,255,0.1)">
            <div
              class="h-1.5 rounded-full"
              style="width: 0%; background: linear-gradient(90deg, #7c3aed, #00b4d8)"
            />
          </div>
          <p class="texto-glass-suave text-xs mt-1">Límite mensual</p>
        </div>
      </div>

      <!-- Diálogo crear/editar -->
      <div
        v-if="dialogoVisible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px)"
        @click.self="dialogoVisible = false"
      >
        <div class="glass w-full max-w-md p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold texto-glass">
              {{ presupuestoEditando ? 'Editar presupuesto' : 'Nuevo presupuesto' }}
            </h3>
            <button
              @click="dialogoVisible = false"
              class="w-8 h-8 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
              style="background: rgba(255,255,255,0.08)"
            >
              <i class="pi pi-times text-sm" />
            </button>
          </div>

          <form @submit.prevent="guardarPresupuesto" class="flex flex-col gap-4">
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
                <option v-for="cat in categorias" :key="cat.id" :value="cat.id" class="bg-gray-900">
                  {{ cat.nombre }}
                </option>
              </select>
              <small class="text-red-400" v-if="errores.id_categoria">{{ errores.id_categoria }}</small>
            </div>

            <!-- Mes -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Mes</label>
              <select
                v-model="formulario.mes"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.mes ? 'border-red-400' : 'focus:border-purple-400'"
              >
                <option value="" class="bg-gray-900">Selecciona un mes</option>
                <option v-for="mes in meses" :key="mes.valor" :value="mes.valor" class="bg-gray-900">
                  {{ mes.etiqueta }}
                </option>
              </select>
              <small class="text-red-400" v-if="errores.mes">{{ errores.mes }}</small>
            </div>

            <!-- Año -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Año</label>
              <select
                v-model="formulario.anio"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.anio ? 'border-red-400' : 'focus:border-purple-400'"
              >
                <option value="" class="bg-gray-900">Selecciona un año</option>
                <option v-for="anio in anios" :key="anio" :value="anio" class="bg-gray-900">
                  {{ anio }}
                </option>
              </select>
              <small class="text-red-400" v-if="errores.anio">{{ errores.anio }}</small>
            </div>

            <!-- Importe límite -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Importe límite</label>
              <input
                v-model="formulario.importe_limite"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.importe_limite ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="text-red-400" v-if="errores.importe_limite">{{ errores.importe_limite }}</small>
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
                <span v-if="!guardando">{{ presupuestoEditando ? 'Guardar cambios' : 'Crear presupuesto' }}</span>
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
          <h3 class="text-lg font-bold texto-glass mb-2">¿Eliminar presupuesto?</h3>
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
              @click="eliminarPresupuesto"
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

const presupuestos = ref([])
const categorias = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const dialogoEliminarVisible = ref(false)
const presupuestoEditando = ref(null)
const presupuestoEliminar = ref(null)
const errores = ref({})

const meses = [
  { etiqueta: 'Enero', valor: 1 }, { etiqueta: 'Febrero', valor: 2 },
  { etiqueta: 'Marzo', valor: 3 }, { etiqueta: 'Abril', valor: 4 },
  { etiqueta: 'Mayo', valor: 5 }, { etiqueta: 'Junio', valor: 6 },
  { etiqueta: 'Julio', valor: 7 }, { etiqueta: 'Agosto', valor: 8 },
  { etiqueta: 'Septiembre', valor: 9 }, { etiqueta: 'Octubre', valor: 10 },
  { etiqueta: 'Noviembre', valor: 11 }, { etiqueta: 'Diciembre', valor: 12 }
]

const anios = computed(() => {
  const anioActual = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => anioActual - i)
})

const formulario = ref({
  id_categoria: '',
  mes: new Date().getMonth() + 1,
  anio: new Date().getFullYear(),
  importe_limite: ''
})

const filtros = ref({ mes: '', anio: '' })

function obtenerNombreCategoria(id) {
  return categorias.value.find(c => c.id === id)?.nombre || '-'
}

function obtenerNombreMes(numero) {
  return meses.find(m => m.valor === numero)?.etiqueta || '-'
}

function formatearMoneda(valor) {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: autenticacion.usuario?.moneda || 'EUR'
  }).format(valor)
}

async function cargarPresupuestos() {
  cargando.value = true
  try {
    const params = {}
    if (filtros.value.mes) params.mes = filtros.value.mes
    if (filtros.value.anio) params.anio = filtros.value.anio
    const respuesta = await api.get('/presupuestos/', { params })
    presupuestos.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los presupuestos', life: 3000 })
  } finally {
    cargando.value = false
  }
}

async function cargarCategorias() {
  const respuesta = await api.get('/categorias/', { params: { tipo: 'gasto' } })
  categorias.value = respuesta.data
}

function abrirDialogo(presupuesto = null) {
  errores.value = {}
  presupuestoEditando.value = presupuesto
  if (presupuesto) {
    formulario.value = {
      id_categoria: presupuesto.id_categoria,
      mes: presupuesto.mes,
      anio: presupuesto.anio,
      importe_limite: presupuesto.importe_limite
    }
  } else {
    formulario.value = {
      id_categoria: '',
      mes: new Date().getMonth() + 1,
      anio: new Date().getFullYear(),
      importe_limite: ''
    }
  }
  dialogoVisible.value = true
}

function validar() {
  errores.value = {}
  if (!formulario.value.id_categoria) errores.value.id_categoria = 'La categoría es obligatoria'
  if (!formulario.value.mes) errores.value.mes = 'El mes es obligatorio'
  if (!formulario.value.anio) errores.value.anio = 'El año es obligatorio'
  if (!formulario.value.importe_limite) errores.value.importe_limite = 'El importe límite es obligatorio'
  return Object.keys(errores.value).length === 0
}

async function guardarPresupuesto() {
  if (!validar()) return
  guardando.value = true
  try {
    const datos = {
      ...formulario.value,
      importe_limite: parseFloat(formulario.value.importe_limite)
    }
    if (presupuestoEditando.value) {
      await api.put(`/presupuestos/${presupuestoEditando.value.id}`, datos)
      toast.add({ severity: 'success', summary: 'Actualizado', detail: 'Presupuesto actualizado correctamente', life: 3000 })
    } else {
      await api.post('/presupuestos/', datos)
      toast.add({ severity: 'success', summary: 'Creado', detail: 'Presupuesto creado correctamente', life: 3000 })
    }
    dialogoVisible.value = false
    await cargarPresupuestos()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al guardar', life: 3000 })
  } finally {
    guardando.value = false
  }
}

function confirmarEliminar(presupuesto) {
  presupuestoEliminar.value = presupuesto
  dialogoEliminarVisible.value = true
}

async function eliminarPresupuesto() {
  try {
    await api.delete(`/presupuestos/${presupuestoEliminar.value.id}`)
    toast.add({ severity: 'success', summary: 'Eliminado', detail: 'Presupuesto eliminado correctamente', life: 3000 })
    dialogoEliminarVisible.value = false
    await cargarPresupuestos()
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar el presupuesto', life: 3000 })
  }
}

onMounted(async () => {
  await Promise.all([cargarPresupuestos(), cargarCategorias()])
})
</script>