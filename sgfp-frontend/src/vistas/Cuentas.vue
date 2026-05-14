<!-- Vista de cuentas con listado y CRUD -->
<!-- Basado en: https://primevue.org/datatable/ -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Cuentas</h2>
          <p class="text-gray-500">Gestiona tus fuentes de dinero</p>
        </div>
        <Button
          label="Nueva cuenta"
          icon="pi pi-plus"
          @click="abrirDialogo()"
        />
      </div>

      <!-- Tarjetas de cuentas -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card
          v-for="cuenta in cuentas"
          :key="cuenta.id"
          class="border-l-4 border-primary-500"
        >
          <template #content>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">{{ obtenerEtiquetaTipo(cuenta.tipo) }}</p>
                <p class="text-xl font-bold text-gray-800">{{ cuenta.nombre }}</p>
                <p class="text-lg font-semibold text-primary-600 mt-1">
                  {{ formatearMoneda(cuenta.saldo_inicial) }}
                </p>
              </div>
              <i :class="obtenerIconoTipo(cuenta.tipo)" class="text-4xl text-primary-300" />
            </div>
            <div class="flex gap-2 mt-4">
              <Button
                icon="pi pi-pencil"
                severity="secondary"
                text
                rounded
                @click="abrirDialogo(cuenta)"
              />
              <Button
                icon="pi pi-trash"
                severity="danger"
                text
                rounded
                @click="confirmarEliminar(cuenta)"
              />
            </div>
          </template>
        </Card>
      </div>

      <!-- Mensaje si no hay cuentas -->
      <Card v-if="!cargando && cuentas.length === 0">
        <template #content>
          <div class="text-center py-8">
            <i class="pi pi-credit-card text-5xl text-gray-300 mb-4" />
            <p class="text-gray-400">No hay cuentas registradas</p>
            <Button
              label="Crear primera cuenta"
              icon="pi pi-plus"
              class="mt-4"
              @click="abrirDialogo()"
            />
          </div>
        </template>
      </Card>

      <!-- Diálogo crear/editar cuenta -->
      <Dialog
        v-model:visible="dialogoVisible"
        :header="cuentaEditando ? 'Editar cuenta' : 'Nueva cuenta'"
        modal
        class="w-full max-w-md"
      >
        <form @submit.prevent="guardarCuenta" class="flex flex-col gap-4">
          <!-- Nombre -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Nombre</label>
            <InputText
              v-model="formulario.nombre"
              placeholder="Ej: Cuenta corriente BBVA"
              :invalid="!!errores.nombre"
              fluid
            />
            <small class="text-red-500" v-if="errores.nombre">{{ errores.nombre }}</small>
          </div>

          <!-- Tipo -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Tipo</label>
            <Select
              v-model="formulario.tipo"
              :options="tiposCuenta"
              optionLabel="etiqueta"
              optionValue="valor"
              placeholder="Selecciona un tipo"
              :invalid="!!errores.tipo"
              fluid
            />
            <small class="text-red-500" v-if="errores.tipo">{{ errores.tipo }}</small>
          </div>

          <!-- Saldo inicial -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Saldo inicial</label>
            <InputNumber
              v-model="formulario.saldo_inicial"
              mode="currency"
              currency="EUR"
              locale="es-ES"
              :invalid="!!errores.saldo_inicial"
              fluid
            />
            <small class="text-red-500" v-if="errores.saldo_inicial">{{ errores.saldo_inicial }}</small>
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
              :label="cuentaEditando ? 'Guardar cambios' : 'Crear cuenta'"
              :loading="guardando"
            />
          </div>
        </form>
      </Dialog>
    </div>
  </LayoutPrincipal>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import { useAutenticacionStore } from '../stores/autenticacion'
import api from '../servicios/api'

const toast = useToast()
const confirm = useConfirm()
const autenticacion = useAutenticacionStore()

// Estado
const cuentas = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const cuentaEditando = ref(null)
const errores = ref({})

// Tipos de cuenta
const tiposCuenta = [
  { etiqueta: 'Efectivo', valor: 'efectivo' },
  { etiqueta: 'Cuenta bancaria', valor: 'bancaria' },
  { etiqueta: 'Tarjeta', valor: 'tarjeta' },
  { etiqueta: 'Ahorro', valor: 'ahorro' }
]

// Formulario
const formulario = ref({
  nombre: '',
  tipo: 'bancaria',
  saldo_inicial: 0
})

// Obtiene la etiqueta del tipo de cuenta
function obtenerEtiquetaTipo(tipo) {
  return tiposCuenta.find(t => t.valor === tipo)?.etiqueta || tipo
}

// Obtiene el icono según el tipo de cuenta
function obtenerIconoTipo(tipo) {
  const iconos = {
    efectivo: 'pi pi-money-bill',
    bancaria: 'pi pi-building-columns',
    tarjeta: 'pi pi-credit-card',
    ahorro: 'pi pi-piggy-bank'
  }
  return iconos[tipo] || 'pi pi-wallet'
}

// Formatea un número como moneda
function formatearMoneda(valor) {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: autenticacion.usuario?.moneda || 'EUR'
  }).format(valor)
}

// Carga las cuentas
async function cargarCuentas() {
  cargando.value = true
  try {
    const respuesta = await api.get('/cuentas/')
    cuentas.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las cuentas', life: 3000 })
  } finally {
    cargando.value = false
  }
}

// Abre el diálogo para crear o editar
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
    formulario.value = {
      nombre: '',
      tipo: 'bancaria',
      saldo_inicial: 0
    }
  }

  dialogoVisible.value = true
}

// Valida el formulario
function validar() {
  errores.value = {}
  if (!formulario.value.nombre) errores.value.nombre = 'El nombre es obligatorio'
  if (!formulario.value.tipo) errores.value.tipo = 'El tipo es obligatorio'
  if (formulario.value.saldo_inicial === null) errores.value.saldo_inicial = 'El saldo inicial es obligatorio'
  return Object.keys(errores.value).length === 0
}

// Guarda la cuenta (crear o editar)
async function guardarCuenta() {
  if (!validar()) return
  guardando.value = true

  try {
    if (cuentaEditando.value) {
      await api.put(`/cuentas/${cuentaEditando.value.id}`, formulario.value)
      toast.add({ severity: 'success', summary: 'Actualizada', detail: 'Cuenta actualizada correctamente', life: 3000 })
    } else {
      await api.post('/cuentas/', formulario.value)
      toast.add({ severity: 'success', summary: 'Creada', detail: 'Cuenta creada correctamente', life: 3000 })
    }

    dialogoVisible.value = false
    await cargarCuentas()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al guardar', life: 3000 })
  } finally {
    guardando.value = false
  }
}

// Confirma y elimina una cuenta
function confirmarEliminar(cuenta) {
  confirm.require({
    message: '¿Estás seguro de que quieres eliminar esta cuenta?',
    header: 'Confirmar eliminación',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Sí, eliminar',
    rejectLabel: 'Cancelar',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await api.delete(`/cuentas/${cuenta.id}`)
        toast.add({ severity: 'success', summary: 'Eliminada', detail: 'Cuenta eliminada correctamente', life: 3000 })
        await cargarCuentas()
      } catch {
        toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar la cuenta', life: 3000 })
      }
    }
  })
}

onMounted(() => cargarCuentas())
</script>