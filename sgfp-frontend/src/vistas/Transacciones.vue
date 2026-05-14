<!-- Vista de transacciones con listado y CRUD -->
<!-- Basado en: https://primevue.org/datatable/ -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Transacciones</h2>
          <p class="text-gray-500">Gestiona tus ingresos y gastos</p>
        </div>
        <Button
          label="Nueva transacción"
          icon="pi pi-plus"
          @click="abrirDialogo()"
        />
      </div>

      <!-- Filtros -->
      <Card class="mb-4">
        <template #content>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Select
              v-model="filtros.tipo"
              :options="tiposTransaccion"
              optionLabel="etiqueta"
              optionValue="valor"
              placeholder="Todos los tipos"
              showClear
              @change="cargarTransacciones"
            />
            <Select
              v-model="filtros.id_categoria"
              :options="categorias"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Todas las categorías"
              showClear
              @change="cargarTransacciones"
            />
            <DatePicker
              v-model="filtros.fecha_inicio"
              placeholder="Fecha inicio"
              dateFormat="dd/mm/yy"
              showClear
              @date-select="cargarTransacciones"
            />
            <DatePicker
              v-model="filtros.fecha_fin"
              placeholder="Fecha fin"
              dateFormat="dd/mm/yy"
              showClear
              @date-select="cargarTransacciones"
            />
          </div>
        </template>
      </Card>

      <!-- Tabla de transacciones -->
      <Card>
        <template #content>
          <DataTable
            :value="transacciones"
            :loading="cargando"
            paginator
            :rows="10"
            stripedRows
            responsiveLayout="scroll"
            emptyMessage="No hay transacciones registradas"
          >
            <Column field="fecha" header="Fecha" sortable>
              <template #body="{ data }">
                {{ formatearFecha(data.fecha) }}
              </template>
            </Column>

            <Column field="tipo" header="Tipo" sortable>
              <template #body="{ data }">
                <Tag
                  :value="data.tipo === 'ingreso' ? 'Ingreso' : 'Gasto'"
                  :severity="data.tipo === 'ingreso' ? 'success' : 'danger'"
                />
              </template>
            </Column>

            <Column field="descripcion" header="Descripción" />

            <Column field="id_categoria" header="Categoría">
              <template #body="{ data }">
                {{ obtenerNombreCategoria(data.id_categoria) }}
              </template>
            </Column>

            <Column field="importe" header="Importe" sortable>
              <template #body="{ data }">
                <span
                  :class="data.tipo === 'ingreso' ? 'text-green-600 font-bold' : 'text-red-600 font-bold'"
                >
                  {{ data.tipo === 'ingreso' ? '+' : '-' }}{{ formatearMoneda(data.importe) }}
                </span>
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

      <!-- Diálogo crear/editar transacción -->
      <Dialog
        v-model:visible="dialogoVisible"
        :header="transaccionEditando ? 'Editar transacción' : 'Nueva transacción'"
        modal
        class="w-full max-w-lg"
      >
        <form @submit.prevent="guardarTransaccion" class="flex flex-col gap-4">
          <!-- Tipo -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Tipo</label>
            <SelectButton
              v-model="formulario.tipo"
              :options="tiposTransaccion"
              optionLabel="etiqueta"
              optionValue="valor"
            />
          </div>

          <!-- Importe -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Importe</label>
            <InputNumber
              v-model="formulario.importe"
              mode="currency"
              currency="EUR"
              locale="es-ES"
              :invalid="!!errores.importe"
              fluid
            />
            <small class="text-red-500" v-if="errores.importe">{{ errores.importe }}</small>
          </div>

          <!-- Fecha -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Fecha</label>
            <DatePicker
              v-model="formulario.fecha"
              dateFormat="dd/mm/yy"
              :invalid="!!errores.fecha"
              fluid
            />
            <small class="text-red-500" v-if="errores.fecha">{{ errores.fecha }}</small>
          </div>

          <!-- Categoría -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Categoría</label>
            <Select
              v-model="formulario.id_categoria"
              :options="categoriasFiltradas"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Selecciona una categoría"
              :invalid="!!errores.id_categoria"
              fluid
            />
            <small class="text-red-500" v-if="errores.id_categoria">{{ errores.id_categoria }}</small>
          </div>

          <!-- Cuenta -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Cuenta</label>
            <Select
              v-model="formulario.id_cuenta"
              :options="cuentas"
              optionLabel="nombre"
              optionValue="id"
              placeholder="Selecciona una cuenta"
              :invalid="!!errores.id_cuenta"
              fluid
            />
            <small class="text-red-500" v-if="errores.id_cuenta">{{ errores.id_cuenta }}</small>
          </div>

          <!-- Descripción -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Descripción (opcional)</label>
            <Textarea
              v-model="formulario.descripcion"
              rows="2"
              placeholder="Descripción de la transacción"
              fluid
            />
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
              :label="transaccionEditando ? 'Guardar cambios' : 'Crear transacción'"
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
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import Select from 'primevue/select'
import SelectButton from 'primevue/selectbutton'
import InputNumber from 'primevue/inputnumber'
import DatePicker from 'primevue/datepicker'
import Textarea from 'primevue/textarea'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import { useAutenticacionStore } from '../stores/autenticacion'
import api from '../servicios/api'

const toast = useToast()
const confirm = useConfirm()
const autenticacion = useAutenticacionStore()

// Estado
const transacciones = ref([])
const categorias = ref([])
const cuentas = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const transaccionEditando = ref(null)
const errores = ref({})

// Tipos de transacción
const tiposTransaccion = [
  { etiqueta: 'Ingreso', valor: 'ingreso' },
  { etiqueta: 'Gasto', valor: 'gasto' }
]

// Filtros
const filtros = ref({
  tipo: null,
  id_categoria: null,
  fecha_inicio: null,
  fecha_fin: null
})

// Formulario
const formulario = ref({
  tipo: 'gasto',
  importe: null,
  fecha: new Date(),
  descripcion: '',
  id_categoria: null,
  id_cuenta: null
})

// Filtra categorías según el tipo seleccionado
const categoriasFiltradas = computed(() => {
  return categorias.value.filter(c => c.tipo === formulario.value.tipo)
})

// Obtiene el nombre de una categoría por ID
function obtenerNombreCategoria(id) {
  return categorias.value.find(c => c.id === id)?.nombre || '-'
}

// Formatea una fecha
function formatearFecha(fecha) {
  return new Date(fecha).toLocaleDateString('es-ES')
}

// Formatea un número como moneda
function formatearMoneda(valor) {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: autenticacion.usuario?.moneda || 'EUR'
  }).format(valor)
}

// Carga las transacciones con los filtros aplicados
async function cargarTransacciones() {
  cargando.value = true
  try {
    const params = {}
    if (filtros.value.tipo) params.tipo = filtros.value.tipo
    if (filtros.value.id_categoria) params.id_categoria = filtros.value.id_categoria
    if (filtros.value.fecha_inicio) params.fecha_inicio = filtros.value.fecha_inicio.toISOString()
    if (filtros.value.fecha_fin) params.fecha_fin = filtros.value.fecha_fin.toISOString()

    const respuesta = await api.get('/transacciones/', { params })
    transacciones.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las transacciones', life: 3000 })
  } finally {
    cargando.value = false
  }
}

// Carga las categorías
async function cargarCategorias() {
  const respuesta = await api.get('/categorias/')
  categorias.value = respuesta.data
}

// Carga las cuentas
async function cargarCuentas() {
  const respuesta = await api.get('/cuentas/')
  cuentas.value = respuesta.data
}

// Abre el diálogo para crear o editar
function abrirDialogo(transaccion = null) {
  errores.value = {}
  transaccionEditando.value = transaccion

  if (transaccion) {
    formulario.value = {
      tipo: transaccion.tipo,
      importe: transaccion.importe,
      fecha: new Date(transaccion.fecha),
      descripcion: transaccion.descripcion || '',
      id_categoria: transaccion.id_categoria,
      id_cuenta: transaccion.id_cuenta
    }
  } else {
    formulario.value = {
      tipo: 'gasto',
      importe: null,
      fecha: new Date(),
      descripcion: '',
      id_categoria: null,
      id_cuenta: null
    }
  }

  dialogoVisible.value = true
}

// Valida el formulario
function validar() {
  errores.value = {}
  if (!formulario.value.importe) errores.value.importe = 'El importe es obligatorio'
  if (!formulario.value.fecha) errores.value.fecha = 'La fecha es obligatoria'
  if (!formulario.value.id_categoria) errores.value.id_categoria = 'La categoría es obligatoria'
  if (!formulario.value.id_cuenta) errores.value.id_cuenta = 'La cuenta es obligatoria'
  return Object.keys(errores.value).length === 0
}

// Guarda la transacción (crear o editar)
async function guardarTransaccion() {
  if (!validar()) return
  guardando.value = true

  try {
    const datos = {
      ...formulario.value,
      fecha: formulario.value.fecha.toISOString()
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

// Confirma y elimina una transacción
function confirmarEliminar(transaccion) {
  confirm.require({
    message: '¿Estás seguro de que quieres eliminar esta transacción?',
    header: 'Confirmar eliminación',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Sí, eliminar',
    rejectLabel: 'Cancelar',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await api.delete(`/transacciones/${transaccion.id}`)
        toast.add({ severity: 'success', summary: 'Eliminada', detail: 'Transacción eliminada correctamente', life: 3000 })
        await cargarTransacciones()
      } catch {
        toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar la transacción', life: 3000 })
      }
    }
  })
}

onMounted(async () => {
  await Promise.all([cargarTransacciones(), cargarCategorias(), cargarCuentas()])
})
</script>