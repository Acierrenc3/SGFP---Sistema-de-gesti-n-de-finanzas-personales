<!-- Vista de categorías con estilo Glassmorphism -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8 animar-lateral">
        <div>
          <h2 class="text-2xl font-bold texto-glass">Categorías</h2>
          <p class="texto-glass-suave text-sm mt-1">Gestiona tus categorías de transacciones</p>
        </div>
        <button
          @click="abrirDialogo()"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-white text-sm font-medium transition-all hover:opacity-90 active:scale-95"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <i class="pi pi-plus" />
          Nueva categoría
        </button>
      </div>

      <!-- Grid de categorías -->
      <div v-if="cargando" class="flex justify-center py-12">
        <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
      </div>

      <div v-else-if="categorias.length === 0" class="glass flex flex-col items-center py-12 texto-glass-suave animar-entrada">
        <i class="pi pi-tag text-4xl mb-2 opacity-30" />
        <p class="text-sm">No hay categorías registradas</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="categoria in categorias"
          :key="categoria.id"
          class="glass p-5 group animar-entrada"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 rounded-xl flex items-center justify-center"
                :style="categoria.color
                  ? `background: ${categoria.color}25; border: 1px solid ${categoria.color}50`
                  : 'background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1)'"
              >
                <i
                  :class="categoria.icono ? `pi ${categoria.icono}` : 'pi pi-tag'"
                  :style="categoria.color ? `color: ${categoria.color}` : 'color: rgba(255,255,255,0.5)'"
                />
              </div>
              <div>
                <p class="texto-glass font-medium text-sm">{{ categoria.nombre }}</p>
                <span
                  class="text-xs px-2 py-0.5 rounded-lg"
                  :style="categoria.tipo === 'ingreso'
                    ? 'background: rgba(74,222,128,0.15); color: #4ade80'
                    : 'background: rgba(248,113,113,0.15); color: #f87171'"
                >
                  {{ categoria.tipo === 'ingreso' ? 'Ingreso' : 'Gasto' }}
                </span>
              </div>
            </div>

            <div
              v-if="categoria.id_usuario"
              class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <button
                @click="abrirDialogo(categoria)"
                class="w-7 h-7 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-pencil text-xs" />
              </button>
              <button
                @click="confirmarEliminar(categoria)"
                class="w-7 h-7 rounded-lg flex items-center justify-center text-red-400/50 hover:text-red-400 transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-trash text-xs" />
              </button>
            </div>

            <span
              v-else
              class="text-xs px-2 py-0.5 rounded-lg texto-glass-suave"
              style="background: rgba(255,255,255,0.08)"
            >
              Predefinida
            </span>
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
        <div class="glass w-full max-w-lg p-6 animar-dialogo overflow-y-auto max-h-screen">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold texto-glass">
              {{ categoriaEditando ? 'Editar categoría' : 'Nueva categoría' }}
            </h3>
            <button
              @click="dialogoVisible = false"
              class="w-8 h-8 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
              style="background: rgba(255,255,255,0.08)"
            >
              <i class="pi pi-times text-sm" />
            </button>
          </div>

          <form @submit.prevent="guardarCategoria" class="flex flex-col gap-4">
            <!-- Nombre -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Nombre</label>
              <input
                v-model="formulario.nombre"
                type="text"
                placeholder="Nombre de la categoría"
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.nombre ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="text-red-400" v-if="errores.nombre">{{ errores.nombre }}</small>
            </div>

            <!-- Tipo -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Tipo</label>
              <div class="flex gap-2">
                <button
                  type="button"
                  v-for="tipo in tiposCategoria"
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

            <!-- Selector visual de iconos -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Icono</label>
              <div class="grid grid-cols-6 gap-2">
                <button
                  type="button"
                  v-for="icono in iconosDisponibles"
                  :key="icono.valor"
                  @click="formulario.icono = icono.valor"
                  class="flex flex-col items-center gap-1 p-2 rounded-xl transition-all"
                  :style="formulario.icono === icono.valor
                    ? `background: ${formulario.color || '#7c3aed'}30; border: 1px solid ${formulario.color || '#7c3aed'}60`
                    : 'background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1)'"
                  :title="icono.etiqueta"
                >
                  <i
                    :class="`pi ${icono.valor} text-lg`"
                    :style="formulario.icono === icono.valor
                      ? `color: ${formulario.color || '#7c3aed'}`
                      : 'color: rgba(255,255,255,0.5)'"
                  />
                  <span class="text-xs texto-glass-suave truncate w-full text-center" style="font-size: 9px">
                    {{ icono.etiqueta }}
                  </span>
                </button>
              </div>
            </div>

            <!-- Color -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Color</label>
              <div class="flex flex-wrap gap-2">
                <button
                  type="button"
                  v-for="color in coloresDisponibles"
                  :key="color"
                  @click="formulario.color = color"
                  class="w-8 h-8 rounded-xl transition-all hover:scale-110"
                  :style="`background: ${color}; ${formulario.color === color ? 'outline: 2px solid white; outline-offset: 2px' : ''}`"
                />
                <!-- Color personalizado -->
                <div class="relative">
                  <input
                    v-model="formulario.color"
                    type="color"
                    class="w-8 h-8 rounded-xl cursor-pointer border-0 outline-none opacity-0 absolute inset-0"
                  />
                  <div
                    class="w-8 h-8 rounded-xl flex items-center justify-center cursor-pointer"
                    style="background: rgba(255,255,255,0.1); border: 1px dashed rgba(255,255,255,0.3)"
                  >
                    <i class="pi pi-palette text-xs texto-glass-suave" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Preview -->
            <div class="flex items-center gap-3 p-3 rounded-xl" style="background: rgba(255,255,255,0.05)">
              <div
                class="w-10 h-10 rounded-xl flex items-center justify-center"
                :style="`background: ${formulario.color}25; border: 1px solid ${formulario.color}50`"
              >
                <i
                  :class="`pi ${formulario.icono || 'pi-tag'} text-lg`"
                  :style="`color: ${formulario.color}`"
                />
              </div>
              <div>
                <p class="texto-glass text-sm font-medium">{{ formulario.nombre || 'Nombre de la categoría' }}</p>
                <span
                  class="text-xs px-2 py-0.5 rounded-lg"
                  :style="formulario.tipo === 'ingreso'
                    ? 'background: rgba(74,222,128,0.15); color: #4ade80'
                    : 'background: rgba(248,113,113,0.15); color: #f87171'"
                >
                  {{ formulario.tipo === 'ingreso' ? 'Ingreso' : 'Gasto' }}
                </span>
              </div>
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
                <span v-if="!guardando">{{ categoriaEditando ? 'Guardar cambios' : 'Crear categoría' }}</span>
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
          <h3 class="text-lg font-bold texto-glass mb-2">¿Eliminar categoría?</h3>
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
              @click="eliminarCategoria"
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
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import api from '../servicios/api'

const toast = useToast()

const categorias = ref([])
const cargando = ref(false)
const guardando = ref(false)
const dialogoVisible = ref(false)
const dialogoEliminarVisible = ref(false)
const categoriaEditando = ref(null)
const categoriaEliminar = ref(null)
const errores = ref({})

const tiposCategoria = [
  { etiqueta: 'Ingreso', valor: 'ingreso' },
  { etiqueta: 'Gasto', valor: 'gasto' }
]

const iconosDisponibles = [
  { valor: 'pi-shopping-cart', etiqueta: 'Compras' },
  { valor: 'pi-car', etiqueta: 'Transporte' },
  { valor: 'pi-home', etiqueta: 'Hogar' },
  { valor: 'pi-heart', etiqueta: 'Salud' },
  { valor: 'pi-star', etiqueta: 'Ocio' },
  { valor: 'pi-book', etiqueta: 'Educación' },
  { valor: 'pi-tag', etiqueta: 'General' },
  { valor: 'pi-briefcase', etiqueta: 'Trabajo' },
  { valor: 'pi-globe', etiqueta: 'Restaurantes' },
  { valor: 'pi-sync', etiqueta: 'Suscripciones' },
  { valor: 'pi-desktop', etiqueta: 'Tecnología' },
  { valor: 'pi-chart-line', etiqueta: 'Inversiones' },
  { valor: 'pi-credit-card', etiqueta: 'Tarjeta' },
  { valor: 'pi-gift', etiqueta: 'Regalos' },
  { valor: 'pi-plane', etiqueta: 'Viajes' },
  { valor: 'pi-user', etiqueta: 'Personal' },
  { valor: 'pi-phone', etiqueta: 'Teléfono' },
  { valor: 'pi-wifi', etiqueta: 'Internet' },
  { valor: 'pi-bolt', etiqueta: 'Electricidad' },
  { valor: 'pi-drop', etiqueta: 'Agua' },
  { valor: 'pi-sun', etiqueta: 'Gas' },
  { valor: 'pi-shield', etiqueta: 'Seguros' },
  { valor: 'pi-wallet', etiqueta: 'Efectivo' },
  { valor: 'pi-plus-circle', etiqueta: 'Otros' }
]

const coloresDisponibles = [
  '#7c3aed', '#00b4d8', '#10b981', '#f59e0b',
  '#ef4444', '#ec4899', '#8b5cf6', '#06b6d4',
  '#f97316', '#6366f1', '#14b8a6', '#84cc16'
]

const formulario = ref({
  nombre: '',
  tipo: 'gasto',
  icono: 'pi-tag',
  color: '#7c3aed'
})

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

function abrirDialogo(categoria = null) {
  errores.value = {}
  categoriaEditando.value = categoria
  if (categoria) {
    formulario.value = {
      nombre: categoria.nombre,
      tipo: categoria.tipo,
      icono: categoria.icono || 'pi-tag',
      color: categoria.color || '#7c3aed'
    }
  } else {
    formulario.value = { nombre: '', tipo: 'gasto', icono: 'pi-tag', color: '#7c3aed' }
  }
  dialogoVisible.value = true
}

function validar() {
  errores.value = {}
  if (!formulario.value.nombre) errores.value.nombre = 'El nombre es obligatorio'
  return Object.keys(errores.value).length === 0
}

async function guardarCategoria() {
  if (!validar()) return
  guardando.value = true
  try {
    const datos = {
      ...formulario.value,
      icono: formulario.value.icono || null,
      color: formulario.value.color || null
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

function confirmarEliminar(categoria) {
  categoriaEliminar.value = categoria
  dialogoEliminarVisible.value = true
}

async function eliminarCategoria() {
  try {
    await api.delete(`/categorias/${categoriaEliminar.value.id}`)
    toast.add({ severity: 'success', summary: 'Eliminada', detail: 'Categoría eliminada correctamente', life: 3000 })
    dialogoEliminarVisible.value = false
    await cargarCategorias()
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'No se pudo eliminar la categoría', life: 3000 })
  }
}

onMounted(() => cargarCategorias())
</script>