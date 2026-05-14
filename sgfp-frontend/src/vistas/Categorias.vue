<!-- Vista de categorías con listado y CRUD -->
<!-- Basado en: https://primevue.org/datatable/ -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">Categorías</h2>
          <p class="text-gray-500">Gestiona tus categorías de transacciones</p>
        </div>
        <Button
          label="Nueva categoría"
          icon="pi pi-plus"
          @click="abrirDialogo()"
        />
      </div>

      <!-- Tabla de categorías -->
      <Card>
        <template #content>
          <DataTable
            :value="categorias"
            :loading="cargando"
            paginator
            :rows="10"
            stripedRows
            responsiveLayout="scroll"
            emptyMessage="No hay categorías registradas"
          >
            <Column field="nombre" header="Nombre" sortable>
              <template #body="{ data }">
                <div class="flex items-center gap-2">
                  <!-- Muestra el color de la categoría -->
                  <span
                    v-if="data.color"
                    class="w-4 h-4 rounded-full inline-block"
                    :style="{ backgroundColor: data.color }"
                  />
                  <i v-if="data.icono" :class="`pi ${data.icono}`" />
                  <span>{{ data.nombre }}</span>
                </div>
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

            <Column field="id_usuario" header="Origen">
              <template #body="{ data }">
                <Tag
                  :value="data.id_usuario ? 'Personalizada' : 'Predefinida'"
                  :severity="data.id_usuario ? 'info' : 'secondary'"
                />
              </template>
            </Column>

            <Column header="Acciones">
              <template #body="{ data }">
                <div class="flex gap-2">
                  <!-- Solo permite editar/eliminar categorías personalizadas -->
                  <Button
                    icon="pi pi-pencil"
                    severity="secondary"
                    text
                    rounded
                    :disabled="!data.id_usuario"
                    @click="abrirDialogo(data)"
                  />
                  <Button
                    icon="pi pi-trash"
                    severity="danger"
                    text
                    rounded
                    :disabled="!data.id_usuario"
                    @click="confirmarEliminar(data)"
                  />
                </div>
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>

      <!-- Diálogo crear/editar categoría -->
      <Dialog
        v-model:visible="dialogoVisible"
        :header="categoriaEditando ? 'Editar categoría' : 'Nueva categoría'"
        modal
        class="w-full max-w-md"
      >
        <form @submit.prevent="guardarCategoria" class="flex flex-col gap-4">
          <!-- Nombre -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Nombre</label>
            <InputText
              v-model="formulario.nombre"
              placeholder="Nombre de la categoría"
              :invalid="!!errores.nombre"
              fluid
            />
            <small class="text-red-500" v-if="errores.nombre">{{ errores.nombre }}</small>
          </div>

          <!-- Tipo -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Tipo</label>
            <SelectButton
              v-model="formulario.tipo"
              :options="tiposCategoria"
              optionLabel="etiqueta"
              optionValue="valor"
            />
          </div>

          <!-- Icono -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Icono (opcional)</label>
            <InputText
              v-model="formulario.icono"
              placeholder="Ej: pi-shopping-cart"
              fluid
            />
            <small class="text-gray-400">Usa nombres de PrimeIcons sin el prefijo 'pi'</small>
          </div>

          <!-- Color -->
          <div class="flex flex-col gap-1">
            <label class="font-medium">Color (opcional)</label>
            <div class="flex items-center gap-2">
              <ColorPicker v-model="formulario.color" />
              <span class="text-sm text-gray-500">{{ formulario.color ? `#${formulario.color}` : 'Sin color' }}</span>
            </div>
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
              :label="categoriaEditando ? 'Guardar cambios' : 'Crear categoría'"
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
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import SelectButton from 'primevue/selectbutton'
import ColorPicker from 'primevue/colorpicker'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import api from '../servicios/api'

const toast = useToast()
const confirm = useConfirm()

// Estado
const categorias = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const categoriaEditando = ref(null)
const errores = ref({})

// Tipos de categoría
const tiposCategoria = [
  { etiqueta: 'Ingreso', valor: 'ingreso' },
  { etiqueta: 'Gasto', valor: 'gasto' }
]

// Formulario
const formulario = ref({
  nombre: '',
  tipo: 'gasto',
  icono: '',
  color: ''
})

// Carga las categorías
async function cargarCategorias() {
  cargando.value = true
  try {
    const respuesta = await api.get('/categorias/')
    categorias.value = respuesta.data
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudieron cargar las categorías', life: 3000 })
  } finally {
    cargando.value = false
  }
}

// Abre el diálogo para crear o editar
function abrirDialogo(categoria = null) {
  errores.value = {}
  categoriaEditando.value = categoria

  if (categoria) {
    formulario.value = {
      nombre: categoria.nombre,
      tipo: categoria.tipo,
      icono: categoria.icono || '',
      color: categoria.color ? categoria.color.replace('#', '') : ''
    }
  } else {
    formulario.value = {
      nombre: '',
      tipo: 'gasto',
      icono: '',
      color: ''
    }
  }

  dialogoVisible.value = true
}

// Valida el formulario
function validar() {
  errores.value = {}
  if (!formulario.value.nombre) errores.value.nombre = 'El nombre es obligatorio'
  return Object.keys(errores.value).length === 0
}

// Guarda la categoría (crear o editar)
async function guardarCategoria() {
  if (!validar()) return
  guardando.value = true

  try {
    const datos = {
      ...formulario.value,
      color: formulario.value.color ? `#${formulario.value.color}` : null,
      icono: formulario.value.icono || null
    }

    if (categoriaEditando.value) {
      await api.put(`/categorias/${categoriaEditando.value.id}`, datos)
      toast.add({ severity: 'success', summary: 'Actualizada', detail: 'Categoría actualizada correctamente', life: 3000 })
    } else {
      await api.post('/categorias/', datos)
      toast.add({ severity: 'success', summary: 'Creada', detail: 'Categoría creada correctamente', life: 3000 })
    }

    dialogoVisible.value = false
    await cargarCategorias()
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al guardar', life: 3000 })
  } finally {
    guardando.value = false
  }
}

// Confirma y elimina una categoría
function confirmarEliminar(categoria) {
  confirm.require({
    message: '¿Estás seguro de que quieres eliminar esta categoría?',
    header: 'Confirmar eliminación',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Sí, eliminar',
    rejectLabel: 'Cancelar',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await api.delete(`/categorias/${categoria.id}`)
        toast.add({ severity: 'success', summary: 'Eliminada', detail: 'Categoría eliminada correctamente', life: 3000 })
        await cargarCategorias()
      } catch {
        toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar la categoría', life: 3000 })
      }
    }
  })
}

onMounted(() => cargarCategorias())
</script>