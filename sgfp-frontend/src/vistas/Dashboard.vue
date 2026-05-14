<!-- Vista del dashboard con resumen financiero -->
<!-- Basado en: https://primevue.org/chart/ -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Dashboard</h2>
          <p class="text-gray-500">Resumen de tus finanzas</p>
        </div>

        <!-- Selector de mes y año -->
        <div class="flex gap-2">
          <Select
            v-model="mesSeleccionado"
            :options="meses"
            optionLabel="etiqueta"
            optionValue="valor"
            placeholder="Mes"
            @change="cargarDatos"
          />
          <Select
            v-model="anioSeleccionado"
            :options="anios"
            placeholder="Año"
            @change="cargarDatos"
          />
        </div>
      </div>

      <!-- Tarjetas de resumen -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <!-- Ingresos -->
        <Card class="border-l-4 border-green-500">
          <template #content>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">Ingresos</p>
                <p class="text-2xl font-bold text-green-600">
                  {{ formatearMoneda(resumen?.balance?.total_ingresos) }}
                </p>
              </div>
              <i class="pi pi-arrow-up text-3xl text-green-400" />
            </div>
          </template>
        </Card>

        <!-- Gastos -->
        <Card class="border-l-4 border-red-500">
          <template #content>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">Gastos</p>
                <p class="text-2xl font-bold text-red-600">
                  {{ formatearMoneda(resumen?.balance?.total_gastos) }}
                </p>
              </div>
              <i class="pi pi-arrow-down text-3xl text-red-400" />
            </div>
          </template>
        </Card>

        <!-- Balance -->
        <Card class="border-l-4 border-blue-500">
          <template #content>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">Balance</p>
                <p
                  class="text-2xl font-bold"
                  :class="resumen?.balance?.balance >= 0 ? 'text-blue-600' : 'text-red-600'"
                >
                  {{ formatearMoneda(resumen?.balance?.balance) }}
                </p>
              </div>
              <i class="pi pi-chart-line text-3xl text-blue-400" />
            </div>
          </template>
        </Card>
      </div>

      <!-- Gráficos -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <!-- Gastos por categoría -->
        <Card>
          <template #title>Gastos por categoría</template>
          <template #content>
            <Chart
              v-if="datosCategorias.labels.length"
              type="doughnut"
              :data="datosCategorias"
              :options="opcionesGrafico"
              class="h-64"
            />
            <p v-else class="text-center text-gray-400 py-8">Sin datos disponibles</p>
          </template>
        </Card>

        <!-- Evolución mensual -->
        <Card>
          <template #title>Evolución mensual</template>
          <template #content>
            <Chart
              v-if="datosEvolucion.labels.length"
              type="bar"
              :data="datosEvolucion"
              :options="opcionesBarras"
              class="h-64"
            />
            <p v-else class="text-center text-gray-400 py-8">Sin datos disponibles</p>
          </template>
        </Card>
      </div>

      <!-- Presupuestos -->
      <Card v-if="resumen?.resumen_presupuestos?.length">
        <template #title>Estado de presupuestos</template>
        <template #content>
          <div class="flex flex-col gap-4">
            <div
              v-for="presupuesto in resumen.resumen_presupuestos"
              :key="presupuesto.id_categoria"
            >
              <div class="flex justify-between mb-1">
                <span class="font-medium">{{ presupuesto.nombre_categoria }}</span>
                <span class="text-sm text-gray-500">
                  {{ formatearMoneda(presupuesto.gasto_actual) }} /
                  {{ formatearMoneda(presupuesto.importe_limite) }}
                </span>
              </div>
              <ProgressBar
                :value="Math.min(presupuesto.porcentaje_usado, 100)"
                :class="presupuesto.porcentaje_usado >= 100 ? 'text-red-500' : ''"
              />
            </div>
          </div>
        </template>
      </Card>
    </div>
  </LayoutPrincipal>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import Chart from 'primevue/chart'
import Select from 'primevue/select'
import ProgressBar from 'primevue/progressbar'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import { useAutenticacionStore } from '../stores/autenticacion'
import api from '../servicios/api'

const toast = useToast()
const autenticacion = useAutenticacionStore()

// Estado
const resumen = ref(null)
const cargando = ref(false)

// Mes y año seleccionados (por defecto el actual)
const ahora = new Date()
const mesSeleccionado = ref(ahora.getMonth() + 1)
const anioSeleccionado = ref(ahora.getFullYear())

// Opciones de mes y año
const meses = [
  { etiqueta: 'Enero', valor: 1 },
  { etiqueta: 'Febrero', valor: 2 },
  { etiqueta: 'Marzo', valor: 3 },
  { etiqueta: 'Abril', valor: 4 },
  { etiqueta: 'Mayo', valor: 5 },
  { etiqueta: 'Junio', valor: 6 },
  { etiqueta: 'Julio', valor: 7 },
  { etiqueta: 'Agosto', valor: 8 },
  { etiqueta: 'Septiembre', valor: 9 },
  { etiqueta: 'Octubre', valor: 10 },
  { etiqueta: 'Noviembre', valor: 11 },
  { etiqueta: 'Diciembre', valor: 12 }
]

const anios = computed(() => {
  const anioActual = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => anioActual - i)
})

// Datos para el gráfico de categorías
const datosCategorias = computed(() => {
  const gastos = resumen.value?.gastos_por_categoria || []
  return {
    labels: gastos.map(g => g.nombre_categoria),
    datasets: [{
      data: gastos.map(g => g.total),
      backgroundColor: [
        '#3B82F6', '#10B981', '#F59E0B', '#EF4444',
        '#8B5CF6', '#EC4899', '#14B8A6', '#F97316'
      ]
    }]
  }
})

// Datos para el gráfico de evolución mensual
const datosEvolucion = computed(() => {
  const evolucion = resumen.value?.evolucion_mensual || []
  return {
    labels: evolucion.map(e => `${e.mes}/${e.anio}`),
    datasets: [
      {
        label: 'Ingresos',
        data: evolucion.map(e => e.total_ingresos),
        backgroundColor: '#10B981'
      },
      {
        label: 'Gastos',
        data: evolucion.map(e => e.total_gastos),
        backgroundColor: '#EF4444'
      }
    ]
  }
})

// Opciones de los gráficos
const opcionesGrafico = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' } }
}

const opcionesBarras = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' } }
}

// Formatea un número como moneda
function formatearMoneda(valor) {
  if (valor === undefined || valor === null) return '0,00 €'
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: autenticacion.usuario?.moneda || 'EUR'
  }).format(valor)
}

// Carga los datos del dashboard
async function cargarDatos() {
  cargando.value = true
  try {
    const respuesta = await api.get('/dashboard/resumen', {
      params: {
        mes: mesSeleccionado.value,
        anio: anioSeleccionado.value
      }
    })
    resumen.value = respuesta.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudieron cargar los datos del dashboard',
      life: 3000
    })
  } finally {
    cargando.value = false
  }
}

onMounted(() => cargarDatos())
</script>