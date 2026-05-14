<!-- Vista de presupuestos con listado y CRUD -->
<!-- Basado en: https://primevue.org/datatable/ -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Presupuestos</h2>
          <p class="text-gray-500">Gestiona tus límites de gasto mensuales</p>
        </div>
        <Button
          label="Nuevo presupuesto"
          icon="pi pi-plus"
          @click="abrirDialogo()"
        />
      </div>

      <!-- Filtros -->
      <Card class="mb-4">
        <template #content>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              v-model="filtros.mes"
              :options="meses"
              optionLabel="etiqueta"
              optionValue="valor"
              placeholder="Todos los meses"
              showClear
              @change="cargarPresupuestos"
            />
            <Select
              v-model="filtros.anio"
              :options="anios"
              placeholder="Todos los años"
              showClear
              @change="cargarPresupuestos"
            />
          </div>
        </template>
      </Card>

      <!-- Tabla de presupuestos -->
      <Card>
        <template #content>
          <DataTable
            :value="presupuestos"
            :loading="cargando"
            paginator
            :rows="10"
            stripedRows
            responsiveLayout="scroll"
            emptyMessage="No hay presupuestos registrados"
          >
            <Column field="id_categoria" header="Categoría" sortable>
              <template #body="{ data }">
                {{ obtenerNombreCategoria(data.id_categoria) }}
              </template>
            </Column>

            <Column field="mes" header="Período" sortable>
              <template #body="{ data }">
                {{ obtenerNombreMes(data.mes) }} {{ data.anio }}
              </template>
            </Column>

            <Column field="importe_limite" header="Límite" sortable>
              <template #body="{ data }">
                <span class="font-bold">{{ formatearMoneda(data.importe_limite) }}</span>
              </template>
            </Column>

            <Column header="Acciones">
              <template #body="{ data }">
                <div class="flex gap-2">
                  <Button
                    icon="pi pi-pencil"
                    severity="secondary"
                    text
                    rounded
                    @click="abrirDialogo(data)"
                  />
                  <Button
                    icon="pi pi-trash"
                    severity="danger"
                    text
                    rounded
                    @click="confirmarEliminar(data)"
                  />
                </div>
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>

      <!-- Diálogo crear/editar presupuesto -->
      <Dialog
        v-model:visible="dialogoVisible"
        :header="presupuestoEditando ? 'Editar presupuesto' : 'Nuevo presupuesto'"
        modal
        class="w-full max-w-md"
      >
        <form @submit.prevent="guardarPresupuesto" class="flex flex-col gap-4">
          <!-- Categoría -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Categoría</label>
            <Select
              v-model="formulario.id_categoria"
              :options="categorias"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Selecciona una categoría"
              :invalid="!!errores.id_categoria"
              fluid
            />
            <small class="text-red-500" v-if="errores.id_categoria">{{ errores.id_categoria }}</small>
          </div>

          <!-- Mes -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Mes</label>
            <Select
              v-model="formulario.mes"
              :options="meses"
              optionLabel="etiqueta"
              optionValue="valor"
              placeholder="Selecciona un mes"
              :invalid="!!errores.mes"
              fluid
            />
            <small class="text-red-500" v-if="errores.mes">{{ errores.mes }}</small>
          </div>

          <!-- Año -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Año</label>
            <Select
              v-model="formulario.anio"
              :options="anios"
              placeholder="Selecciona un año"
              :invalid="!!errores.anio"
              fluid
            />
            <small class="text-red-500" v-if="errores.anio">{{ errores.anio }}</small>
          </div>

          <!-- Importe límite -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Importe límite</label>
            <InputNumber
              v-model="formulario.importe_limite"
              mode="currency"
              currency="EUR"
              locale="es-ES"
              :invalid="!!errores.importe_limite"
              fluid
            />
            <small class="text-red-500" v-if="errores.importe_limite">{{ errores.importe_limite }}</small>
          </div>

          <!-- Botones -->
          <div class="flex justify-end gap-2 mt-2">
            <Button
              label="Cancelar"
              severity="secondary"
              @click="dialogoVisible = false"
            />
            <Button
              type="submit"
              :label="presupuestoEditando ? 'Guardar cambios' : 'Crear presupuesto'"
              :loading="guardando"
            />
          </div>
        </form>
      </Dialog>
    </div>
  </LayoutPrincipal>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Card from 'primevue/card'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import Select from 'primevue/select'
import InputNumber from 'primevue/inputnumber'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import { useAutenticacionStore } from '../stores/autenticacion'
import api from '../servicios/api'

const toast = useToast()
const confirm = useConfirm()
const autenticacion = useAutenticacionStore()

// Estado
const presupuestos = ref([])
const categorias = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const presupuestoEditando = ref(null)
const errores = ref({})

// Opciones de mes
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

// Opciones de año
const anios = computed(() => {
  const anioActual = new Date().getFullYear()
  return Array.from({ length: 5 }, (_, i) => anioActual - i)
})

// Formulario
const formulario = ref({
  id_categoria: null,
  mes: new Date().getMonth() + 1,
  anio: new Date().getFullYear(),
  importe_limite: null
})

// Filtros
const filtros = ref({
  mes: null,
  anio: null
})

// Obtiene el nombre de una categoría por ID
function obtenerNombreCategoria(id) {
  return categorias.value.find(c => c.id === id)?.nombre || '-'
}

// Obtiene el nombre de un mes por número
function obtenerNombreMes(numero) {
  return meses.find(m => m.valor === numero)?.etiqueta || '-'
}

// Formatea un número como moneda
function formatearMoneda(valor) {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: autenticacion.usuario?.moneda || 'EUR'
  }).format(valor)
}

// Carga los presupuestos
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

// Carga las categorías de tipo gasto
async function cargarCategorias() {
  const respuesta = await api.get('/categorias/', { params: { tipo: 'gasto' } })
  categorias.value = respuesta.data
}

// Abre el diálogo para crear o editar
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
      id_categoria: null,
      mes: new Date().getMonth() + 1,
      anio: new Date().getFullYear(),
      importe_limite: null
    }
  }

  dialogoVisible.value = true
}

// Valida el formulario
function validar() {
  errores.value = {}
  if (!formulario.value.id_categoria) errores.value.id_categoria = 'La categoría es obligatoria'
  if (!formulario.value.mes) errores.value.mes = 'El mes es obligatorio'
  if (!formulario.value.anio) errores.value.anio = 'El año es obligatorio'
  if (!formulario.value.importe_limite) errores.value.importe_limite = 'El importe límite es obligatorio'
  return Object.keys(errores.value).length === 0
}

// Guarda el presupuesto (crear o editar)
async function guardarPresupuesto() {
  if (!validar()) return
  guardando.value = true

  try {
    if (presupuestoEditando.value) {
      await api.put(`/presupuestos/${presupuestoEditando.value.id}`, formulario.value)
      toast.add({ severity: 'success', summary: 'Actualizado', detail: 'Presupuesto actualizado correctamente', life: 3000 })
    } else {
      await api.post('/presupuestos/', formulario.value)
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

// Confirma y elimina un presupuesto
function confirmarEliminar(presupuesto) {
  confirm.require({
    message: '¿Estás seguro de que quieres eliminar este presupuesto?',
    header: 'Confirmar eliminación',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Sí, eliminar',
    rejectLabel: 'Cancelar',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await api.delete(`/presupuestos/${presupuesto.id}`)
        toast.add({ severity: 'success', summary: 'Eliminado', detail: 'Presupuesto eliminado correctamente', life: 3000 })
        await cargarPresupuestos()
      } catch {
        toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar el presupuesto', life: 3000 })
      }
    }
  })
}

onMounted(async () => {
  await Promise.all([cargarPresupuestos(), cargarCategorias()])
})
</script>