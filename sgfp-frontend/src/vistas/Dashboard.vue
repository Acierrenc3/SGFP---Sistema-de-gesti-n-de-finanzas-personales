<!-- Vista del dashboard con estilo Glassmorphism -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8 animar-lateral">
        <div>
          <h2 class="text-2xl font-bold texto-glass">Dashboard</h2>
          <p class="texto-glass-suave text-sm mt-1">Resumen de tus finanzas</p>
        </div>

        <!-- Selector de mes y año -->
        <div class="flex gap-2">
          <select
            v-model="mesSeleccionado"
            @change="cargarDatos"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option v-for="mes in meses" :key="mes.valor" :value="mes.valor" class="bg-gray-900">
              {{ mes.etiqueta }}
            </option>
          </select>
          <select
            v-model="anioSeleccionado"
            @change="cargarDatos"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option v-for="anio in anios" :key="anio" :value="anio" class="bg-gray-900">
              {{ anio }}
            </option>
          </select>
        </div>
      </div>

      <!-- Tarjetas de resumen -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <!-- Ingresos -->
        <div class="glass p-6 animar-entrada">
          <div class="flex items-center justify-between">
            <div>
              <p class="texto-glass-suave text-sm mb-1">Ingresos</p>
              <p class="text-2xl font-bold text-green-400">
                {{ formatearMoneda(resumen?.balance?.total_ingresos) }}
              </p>
            </div>
            <div class="w-12 h-12 rounded-xl flex items-center justify-center"
              style="background: rgba(74,222,128,0.15)">
              <i class="pi pi-arrow-up text-green-400 text-xl" />
            </div>
          </div>
        </div>

        <!-- Gastos -->
        <div class="glass p-6 animar-entrada">
          <div class="flex items-center justify-between">
            <div>
              <p class="texto-glass-suave text-sm mb-1">Gastos</p>
              <p class="text-2xl font-bold text-red-400">
                {{ formatearMoneda(resumen?.balance?.total_gastos) }}
              </p>
            </div>
            <div class="w-12 h-12 rounded-xl flex items-center justify-center"
              style="background: rgba(248,113,113,0.15)">
              <i class="pi pi-arrow-down text-red-400 text-xl" />
            </div>
          </div>
        </div>

        <!-- Balance -->
        <div class="glass p-6 animar-entrada">
          <div class="flex items-center justify-between">
            <div>
              <p class="texto-glass-suave text-sm mb-1">Balance</p>
              <p
                class="text-2xl font-bold"
                :class="(resumen?.balance?.balance ?? 0) >= 0 ? 'text-purple-400' : 'text-red-400'"
              >
                {{ formatearMoneda(resumen?.balance?.balance) }}
              </p>
            </div>
            <div class="w-12 h-12 rounded-xl flex items-center justify-center"
              style="background: rgba(124,58,237,0.15)">
              <i class="pi pi-chart-line text-purple-400 text-xl" />
            </div>
          </div>
        </div>
      </div>

      <!-- Gráficos -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <!-- Gastos por categoría -->
        <div class="glass p-6 animar-entrada">
          <h3 class="texto-glass font-semibold mb-4">Gastos por categoría</h3>
          <Chart
            v-if="datosCategorias.labels.length"
            type="doughnut"
            :data="datosCategorias"
            :options="opcionesGrafico"
            class="h-64"
          />
          <div v-else class="flex flex-col items-center justify-center h-64 texto-glass-suave">
            <i class="pi pi-chart-pie text-4xl mb-2 opacity-30" />
            <p class="text-sm">Sin datos disponibles</p>
          </div>
        </div>

        <!-- Evolución mensual -->
        <div class="glass p-6 animar-entrada">
          <h3 class="texto-glass font-semibold mb-4">Evolución mensual</h3>
          <Chart
            v-if="datosEvolucion.labels.length"
            type="bar"
            :data="datosEvolucion"
            :options="opcionesBarras"
            class="h-64"
          />
          <div v-else class="flex flex-col items-center justify-center h-64 texto-glass-suave">
            <i class="pi pi-chart-bar text-4xl mb-2 opacity-30" />
            <p class="text-sm">Sin datos disponibles</p>
          </div>
        </div>
      </div>

      <!-- Presupuestos -->
      <div class="glass p-6 animar-entrada" v-if="resumen?.resumen_presupuestos?.length">
        <h3 class="texto-glass font-semibold mb-4">Estado de presupuestos</h3>
        <div class="flex flex-col gap-4">
          <div
            v-for="presupuesto in resumen.resumen_presupuestos"
            :key="presupuesto.id_categoria"
          >
            <div class="flex justify-between mb-2">
              <span class="texto-glass text-sm font-medium">{{ presupuesto.nombre_categoria }}</span>
              <span class="texto-glass-suave text-sm">
                {{ formatearMoneda(presupuesto.gasto_actual) }} /
                {{ formatearMoneda(presupuesto.importe_limite) }}
              </span>
            </div>
            <div class="w-full h-2 rounded-full" style="background: rgba(255,255,255,0.1)">
              <div
                class="h-2 rounded-full animar-progreso"
                :style="{
                  width: `${Math.min(presupuesto.porcentaje_usado, 100)}%`,
                  background: presupuesto.porcentaje_usado >= 100
                    ? 'linear-gradient(90deg, #ef4444, #dc2626)'
                    : presupuesto.porcentaje_usado >= 80
                    ? 'linear-gradient(90deg, #f59e0b, #d97706)'
                    : 'linear-gradient(90deg, #7c3aed, #00b4d8)'
                }"
              />
            </div>
            <p class="text-xs texto-glass-suave mt-1">{{ presupuesto.porcentaje_usado.toFixed(1) }}% usado</p>
          </div>
        </div>
      </div>
    </div>
  </LayoutPrincipal>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Chart from 'primevue/chart'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import { useAutenticacionStore } from '../stores/autenticacion'
import api from '../servicios/api'

const toast = useToast()
const autenticacion = useAutenticacionStore()

const resumen = ref(null)
const cargando = ref(false)

const ahora = new Date()
const mesSeleccionado = ref(ahora.getMonth() + 1)
const anioSeleccionado = ref(ahora.getFullYear())

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

const datosCategorias = computed(() => {
  const gastos = resumen.value?.gastos_por_categoria || []
  return {
    labels: gastos.map(g => g.nombre_categoria),
    datasets: [{
      data: gastos.map(g => g.total),
      backgroundColor: ['#7c3aed', '#00b4d8', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#8b5cf6', '#06b6d4'],
      borderWidth: 0
    }]
  }
})

const datosEvolucion = computed(() => {
  const evolucion = resumen.value?.evolucion_mensual || []
  return {
    labels: evolucion.map(e => `${e.mes}/${e.anio}`),
    datasets: [
      {
        label: 'Ingresos',
        data: evolucion.map(e => e.total_ingresos),
        backgroundColor: 'rgba(16,185,129,0.7)',
        borderRadius: 6
      },
      {
        label: 'Gastos',
        data: evolucion.map(e => e.total_gastos),
        backgroundColor: 'rgba(239,68,68,0.7)',
        borderRadius: 6
      }
    ]
  }
})

const opcionesGrafico = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: 'rgba(255,255,255,0.7)', padding: 16, font: { size: 12 } }
    }
  }
}

const opcionesBarras = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: 'rgba(255,255,255,0.7)', padding: 16, font: { size: 12 } }
    }
  },
  scales: {
    x: { ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' } },
    y: { ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' } }
  }
}

function formatearMoneda(valor) {
  if (valor === undefined || valor === null) return '0,00 €'
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: autenticacion.usuario?.moneda || 'EUR'
  }).format(valor)
}

async function cargarDatos() {
  cargando.value = true
  try {
    const respuesta = await api.get('/dashboard/resumen', {
      params: { mes: mesSeleccionado.value, anio: anioSeleccionado.value }
    })
    resumen.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar los datos', life: 3000 })
  } finally {
    cargando.value = false
  }
}

onMounted(() => cargarDatos())
</script>