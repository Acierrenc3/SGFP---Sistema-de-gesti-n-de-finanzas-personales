<!-- Vista de cuentas con estilo Glassmorphism y saldo dinámico -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-2xl font-bold texto-glass">Cuentas</h2>
          <p class="texto-glass-suave text-sm mt-1">Gestiona tus fuentes de dinero</p>
        </div>
        <button
          @click="abrirDialogo()"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-white text-sm font-medium transition-all hover:opacity-90 active:scale-95"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <i class="pi pi-plus" />
          Nueva cuenta
        </button>
      </div>

      <!-- Resumen total -->
<div class="glass p-5 mb-6" v-if="saldos.length">
  <div class="flex items-center justify-between">
    <div>
      <div class="flex items-center gap-2 mb-1">
        <p class="texto-glass-suave text-sm">Patrimonio total</p>
        <button
          @click="cantidadesOcultas = !cantidadesOcultas"
          class="texto-glass-suave hover:text-white transition-colors"
        >
          <i :class="cantidadesOcultas ? 'pi pi-eye-slash' : 'pi pi-eye'" class="text-sm" />
        </button>
      </div>
      <p class="text-3xl font-bold texto-glass">{{ formatearOculto(patrimonioTotal) }}</p>
    </div>
    <div
      class="w-14 h-14 rounded-xl flex items-center justify-center"
      style="background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(0,180,216,0.3))"
    >
      <i class="pi pi-chart-line text-white text-2xl" />
    </div>
  </div>
</div>

      <!-- Grid de cuentas -->
      <div v-if="cargando" class="flex justify-center py-12">
        <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
      </div>

      <div v-else-if="saldos.length === 0" class="glass flex flex-col items-center py-12 texto-glass-suave">
        <i class="pi pi-credit-card text-4xl mb-2 opacity-30" />
        <p class="text-sm mb-4">No hay cuentas registradas</p>
        <button
          @click="abrirDialogo()"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-white text-sm font-medium transition-all hover:opacity-90"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <i class="pi pi-plus" />
          Crear primera cuenta
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="cuenta in saldos"
          :key="cuenta.id"
          class="glass p-6 group"
        >
          <!-- Icono y acciones -->
          <div class="flex items-center justify-between mb-4">
            <div
              class="w-12 h-12 rounded-xl flex items-center justify-center"
              style="background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(0,180,216,0.3)); border: 1px solid rgba(255,255,255,0.1)"
            >
              <i :class="obtenerIconoTipo(cuenta.tipo)" class="text-xl text-white" />
            </div>
            <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                @click="abrirDialogo(cuenta)"
                class="w-7 h-7 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-pencil text-xs" />
              </button>
              <button
                @click="confirmarEliminar(cuenta)"
                class="w-7 h-7 rounded-lg flex items-center justify-center text-red-400/50 hover:text-red-400 transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-trash text-xs" />
              </button>
            </div>
          </div>

          <!-- Nombre y tipo -->
          <p class="texto-glass font-semibold text-lg mb-1">{{ cuenta.nombre }}</p>
          <p class="texto-glass-suave text-xs mb-4">{{ obtenerEtiquetaTipo(cuenta.tipo) }}</p>

      <!-- Saldo actual -->
      <div style="border-top: 1px solid rgba(255,255,255,0.08)" class="pt-4">
        <p class="texto-glass-suave text-xs mb-1">Saldo actual</p>
        <p
          class="text-2xl font-bold"
          :class="cuenta.saldo_actual >= 0 ? 'texto-glass' : 'text-red-400'"
        >
          {{ formatearOculto(cuenta.saldo_actual) }}
        </p>

        <!-- Desglose -->
        <div class="flex gap-4 mt-3">
          <div>
            <p class="text-xs texto-glass-suave">Ingresos</p>
            <p class="text-sm text-green-400 font-medium">+{{ formatearOculto(cuenta.total_ingresos) }}</p>
          </div>
          <div>
            <p class="text-xs texto-glass-suave">Gastos</p>
            <p class="text-sm text-red-400 font-medium">-{{ formatearOculto(cuenta.total_gastos) }}</p>
          </div>
          <div>
            <p class="text-xs texto-glass-suave">Inicial</p>
            <p class="text-sm texto-glass font-medium">{{ formatearOculto(cuenta.saldo_inicial) }}</p>
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
        <div class="glass w-full max-w-md p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold texto-glass">
              {{ cuentaEditando ? 'Editar cuenta' : 'Nueva cuenta' }}
            </h3>
            <button
              @click="dialogoVisible = false"
              class="w-8 h-8 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
              style="background: rgba(255,255,255,0.08)"
            >
              <i class="pi pi-times text-sm" />
            </button>
          </div>

          <form @submit.prevent="guardarCuenta" class="flex flex-col gap-4">
            <!-- Nombre -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Nombre</label>
              <input
                v-model="formulario.nombre"
                type="text"
                placeholder="Ej: Cuenta corriente BBVA"
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.nombre ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="text-red-400" v-if="errores.nombre">{{ errores.nombre }}</small>
            </div>

            <!-- Tipo -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Tipo</label>
              <div class="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  v-for="tipo in tiposCuenta"
                  :key="tipo.valor"
                  @click="formulario.tipo = tipo.valor"
                  class="flex items-center gap-2 px-3 py-2 rounded-xl text-sm transition-all"
                  :style="formulario.tipo === tipo.valor
                    ? 'background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(0,180,216,0.3)); color: white; border: 1px solid rgba(124,58,237,0.5)'
                    : 'background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.1)'"
                >
                  <i :class="obtenerIconoTipo(tipo.valor)" class="text-sm" />
                  {{ tipo.etiqueta }}
                </button>
              </div>
              <small class="text-red-400" v-if="errores.tipo">{{ errores.tipo }}</small>
            </div>

            <!-- Saldo inicial -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Saldo inicial</label>
              <input
                v-model="formulario.saldo_inicial"
                type="number"
                step="0.01"
                placeholder="0.00"
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.saldo_inicial ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="texto-glass-suave text-xs">El saldo actual se calculará automáticamente con tus transacciones</small>
              <small class="text-red-400" v-if="errores.saldo_inicial">{{ errores.saldo_inicial }}</small>
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
                <span v-if="!guardando">{{ cuentaEditando ? 'Guardar cambios' : 'Crear cuenta' }}</span>
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
          <h3 class="text-lg font-bold texto-glass mb-2">¿Eliminar cuenta?</h3>
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
              @click="eliminarCuenta"
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

const saldos = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const dialogoEliminarVisible = ref(false)
const cuentaEditando = ref(null)
const cuentaEliminar = ref(null)
const errores = ref({})

const cantidadesOcultas = ref(false)

function formatearOculto(valor) {
  return cantidadesOcultas.value ? '••••••' : formatearMoneda(valor)
}
const tiposCuenta = [
  { etiqueta: 'Efectivo', valor: 'efectivo' },
  { etiqueta: 'Bancaria', valor: 'bancaria' },
  { etiqueta: 'Tarjeta', valor: 'tarjeta' },
  { etiqueta: 'Ahorro', valor: 'ahorro' }
]

const formulario = ref({
  nombre: '',
  tipo: 'bancaria',
  saldo_inicial: 0
})

// Patrimonio total: suma de saldos actuales de todas las cuentas
const patrimonioTotal = computed(() => {
  return saldos.value.reduce((total, cuenta) => total + cuenta.saldo_actual, 0)
})

function obtenerEtiquetaTipo(tipo) {
  return tiposCuenta.find(t => t.valor === tipo)?.etiqueta || tipo
}

function obtenerIconoTipo(tipo) {
  const iconos = {
    efectivo: 'pi pi-money-bill',
    bancaria: 'pi pi-building-columns',
    tarjeta: 'pi pi-credit-card',
    ahorro: 'pi pi-star'
  }
  return iconos[tipo] || 'pi pi-wallet'
}

function formatearMoneda(valor) {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: autenticacion.usuario?.moneda || 'EUR'
  }).format(valor)
}

// Carga los saldos de todas las cuentas
async function cargarSaldos() {
  cargando.value = true
  try {
    const respuesta = await api.get('/cuentas/saldos/resumen')
    saldos.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las cuentas', life: 3000 })
  } finally {
    cargando.value = false
  }
}

function abrirDialogo(cuenta = null) {
  errores.value = {}
  cuentaEditando.value = cuenta
  if (cuenta) {
    formulario.value = {
      nombre: cuenta.nombre,
      tipo: cuenta.tipo,
      saldo_inicial: cuenta.saldo_inicial
    }
  } else {
    formulario.value = { nombre: '', tipo: 'bancaria', saldo_inicial: 0 }
  }
  dialogoVisible.value = true
}

function validar() {
  errores.value = {}
  if (!formulario.value.nombre) errores.value.nombre = 'El nombre es obligatorio'
  if (!formulario.value.tipo) errores.value.tipo = 'El tipo es obligatorio'
  if (formulario.value.saldo_inicial === null || formulario.value.saldo_inicial === '') {
    errores.value.saldo_inicial = 'El saldo inicial es obligatorio'
  }
  return Object.keys(errores.value).length === 0
}

async function guardarCuenta() {
  if (!validar()) return
  guardando.value = true
  try {
    const datos = {
      ...formulario.value,
      saldo_inicial: parseFloat(formulario.value.saldo_inicial)
    }
    if (cuentaEditando.value) {
      await api.put(`/cuentas/${cuentaEditando.value.id}`, datos)
      toast.add({ severity: 'success', summary: 'Actualizada', detail: 'Cuenta actualizada correctamente', life: 3000 })
    } else {
      await api.post('/cuentas/', datos)
      toast.add({ severity: 'success', summary: 'Creada', detail: 'Cuenta creada correctamente', life: 3000 })
    }
    dialogoVisible.value = false
    await cargarSaldos()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al guardar', life: 3000 })
  } finally {
    guardando.value = false
  }
}

function confirmarEliminar(cuenta) {
  cuentaEliminar.value = cuenta
  dialogoEliminarVisible.value = true
}

async function eliminarCuenta() {
  try {
    await api.delete(`/cuentas/${cuentaEliminar.value.id}`)
    toast.add({ severity: 'success', summary: 'Eliminada', detail: 'Cuenta eliminada correctamente', life: 3000 })
    dialogoEliminarVisible.value = false
    await cargarSaldos()
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar la cuenta', life: 3000 })
  }
}

onMounted(() => cargarSaldos())
</script>