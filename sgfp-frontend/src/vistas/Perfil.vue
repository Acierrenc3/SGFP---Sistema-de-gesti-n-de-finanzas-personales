<!-- Vista del perfil con estilo Glassmorphism -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold texto-glass">Perfil</h2>
        <p class="texto-glass-suave text-sm mt-1">Gestiona tu información personal</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Tarjeta información personal -->
        <div class="glass p-6">
          <!-- Avatar -->
          <div class="flex flex-col items-center mb-6">
            <div
              class="w-20 h-20 rounded-2xl flex items-center justify-center text-3xl font-bold text-white mb-3"
              style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
            >
              {{ inicialUsuario }}
            </div>
            <p class="texto-glass font-semibold">{{ autenticacion.usuario?.nombre }}</p>
            <p class="texto-glass-suave text-sm">{{ autenticacion.usuario?.email }}</p>
          </div>

          <form @submit.prevent="guardarPerfil" class="flex flex-col gap-4">
            <!-- Nombre -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Nombre</label>
              <div class="relative">
                <i class="pi pi-user absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave text-sm" />
                <input
                  v-model="formulario.nombre"
                  type="text"
                  placeholder="Tu nombre"
                  class="w-full pl-9 pr-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                  style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                  :class="errores.nombre ? 'border-red-400' : 'focus:border-purple-400'"
                />
              </div>
              <small class="text-red-400" v-if="errores.nombre">{{ errores.nombre }}</small>
            </div>

            <!-- Email (solo lectura) -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Email</label>
              <div class="relative">
                <i class="pi pi-envelope absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave text-sm" />
                <input
                  :value="autenticacion.usuario?.email"
                  type="email"
                  disabled
                  class="w-full pl-9 pr-4 py-3 rounded-xl texto-glass-suave outline-none cursor-not-allowed"
                  style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08)"
                />
              </div>
              <small class="texto-glass-suave text-xs">El email no se puede modificar</small>
            </div>

            <!-- Moneda -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Moneda</label>
              <select
                v-model="formulario.moneda"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
              >
                <option v-for="moneda in monedas" :key="moneda.valor" :value="moneda.valor" class="bg-gray-900">
                  {{ moneda.etiqueta }}
                </option>
              </select>
            </div>

            <!-- Zona horaria -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Zona horaria</label>
              <select
                v-model="formulario.zona_horaria"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
              >
                <option v-for="zona in zonasHorarias" :key="zona.valor" :value="zona.valor" class="bg-gray-900">
                  {{ zona.etiqueta }}
                </option>
              </select>
            </div>

            <!-- Mensaje éxito -->
            <div
              v-if="mensajeExito"
              class="flex items-center gap-2 px-4 py-3 rounded-xl text-green-400 text-sm"
              style="background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2)"
            >
              <i class="pi pi-check-circle" />
              {{ mensajeExito }}
            </div>

            <!-- Botón guardar -->
            <button
              type="submit"
              :disabled="guardando"
              class="w-full py-3 rounded-xl font-semibold text-white transition-all hover:opacity-90 disabled:opacity-50"
              style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
            >
              <span v-if="!guardando" class="flex items-center justify-center gap-2">
                <i class="pi pi-save" />
                Guardar cambios
              </span>
              <i v-else class="pi pi-spin pi-spinner" />
            </button>
          </form>
        </div>

        <!-- Tarjeta cambio de contraseña -->
        <div class="glass p-6">
          <div class="flex items-center gap-3 mb-6">
            <div
              class="w-10 h-10 rounded-xl flex items-center justify-center"
              style="background: rgba(124,58,237,0.2); border: 1px solid rgba(124,58,237,0.3)"
            >
              <i class="pi pi-lock text-purple-400" />
            </div>
            <div>
              <p class="texto-glass font-semibold">Cambiar contraseña</p>
              <p class="texto-glass-suave text-xs">Actualiza tu contraseña de acceso</p>
            </div>
          </div>

          <form @submit.prevent="cambiarContrasena" class="flex flex-col gap-4">
            <!-- Nueva contraseña -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Nueva contraseña</label>
              <div class="relative">
                <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave text-sm" />
                <input
                  v-model="formularioContrasena.contrasena"
                  :type="mostrarContrasena ? 'text' : 'password'"
                  placeholder="Mínimo 6 caracteres"
                  class="w-full pl-9 pr-10 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                  style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                  :class="erroresContrasena.contrasena ? 'border-red-400' : 'focus:border-purple-400'"
                />
                <button
                  type="button"
                  @click="mostrarContrasena = !mostrarContrasena"
                  class="absolute right-3 top-1/2 -translate-y-1/2 texto-glass-suave hover:text-white transition-colors"
                >
                  <i :class="mostrarContrasena ? 'pi pi-eye-slash' : 'pi pi-eye'" class="text-sm" />
                </button>
              </div>
              <small class="text-red-400" v-if="erroresContrasena.contrasena">{{ erroresContrasena.contrasena }}</small>
            </div>

            <!-- Confirmar contraseña -->
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Confirmar nueva contraseña</label>
              <div class="relative">
                <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave text-sm" />
                <input
                  v-model="formularioContrasena.confirmarContrasena"
                  :type="mostrarConfirmar ? 'text' : 'password'"
                  placeholder="Repite la nueva contraseña"
                  class="w-full pl-9 pr-10 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                  style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                  :class="erroresContrasena.confirmarContrasena ? 'border-red-400' : 'focus:border-purple-400'"
                />
                <button
                  type="button"
                  @click="mostrarConfirmar = !mostrarConfirmar"
                  class="absolute right-3 top-1/2 -translate-y-1/2 texto-glass-suave hover:text-white transition-colors"
                >
                  <i :class="mostrarConfirmar ? 'pi pi-eye-slash' : 'pi pi-eye'" class="text-sm" />
                </button>
              </div>
              <small class="text-red-400" v-if="erroresContrasena.confirmarContrasena">
                {{ erroresContrasena.confirmarContrasena }}
              </small>
            </div>

            <!-- Mensaje éxito -->
            <div
              v-if="mensajeExitoContrasena"
              class="flex items-center gap-2 px-4 py-3 rounded-xl text-green-400 text-sm"
              style="background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2)"
            >
              <i class="pi pi-check-circle" />
              {{ mensajeExitoContrasena }}
            </div>

            <!-- Botón guardar -->
            <button
              type="submit"
              :disabled="guardandoContrasena"
              class="w-full py-3 rounded-xl font-semibold text-white transition-all hover:opacity-90 disabled:opacity-50 mt-2"
              style="background: rgba(124,58,237,0.3); border: 1px solid rgba(124,58,237,0.4)"
            >
              <span v-if="!guardandoContrasena" class="flex items-center justify-center gap-2">
                <i class="pi pi-lock" />
                Cambiar contraseña
              </span>
              <i v-else class="pi pi-spin pi-spinner" />
            </button>
          </form>
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

const guardando = ref(false)
const guardandoContrasena = ref(false)
const errores = ref({})
const erroresContrasena = ref({})
const mensajeExito = ref('')
const mensajeExitoContrasena = ref('')
const mostrarContrasena = ref(false)
const mostrarConfirmar = ref(false)

const formulario = ref({
  nombre: '',
  moneda: 'EUR',
  zona_horaria: 'Europe/Madrid'
})

const formularioContrasena = ref({
  contrasena: '',
  confirmarContrasena: ''
})

const monedas = [
  { etiqueta: 'Euro (€)', valor: 'EUR' },
  { etiqueta: 'Dólar ($)', valor: 'USD' },
  { etiqueta: 'Libra (£)', valor: 'GBP' },
  { etiqueta: 'Franco suizo (CHF)', valor: 'CHF' }
]

const zonasHorarias = [
  { etiqueta: 'Atlántico/Canarias', valor: 'Atlantic/Canary' },
  { etiqueta: 'Europa/Madrid', valor: 'Europe/Madrid' },
  { etiqueta: 'Europa/Londres', valor: 'Europe/London' },
  { etiqueta: 'Europa/París', valor: 'Europe/Paris' },
  { etiqueta: 'América/Nueva York', valor: 'America/New_York' },
  { etiqueta: 'América/Los Ángeles', valor: 'America/Los_Angeles' }
]

const inicialUsuario = computed(() => {
  return autenticacion.usuario?.nombre?.charAt(0).toUpperCase() || 'U'
})

function cargarDatosPerfil() {
  if (autenticacion.usuario) {
    formulario.value = {
      nombre: autenticacion.usuario.nombre,
      moneda: autenticacion.usuario.moneda,
      zona_horaria: autenticacion.usuario.zona_horaria
    }
  }
}

function validar() {
  errores.value = {}
  if (!formulario.value.nombre) errores.value.nombre = 'El nombre es obligatorio'
  return Object.keys(errores.value).length === 0
}

async function guardarPerfil() {
  if (!validar()) return
  guardando.value = true
  mensajeExito.value = ''
  try {
    await api.put('/usuarios/perfil', formulario.value)
    await autenticacion.obtenerPerfil()
    mensajeExito.value = 'Perfil actualizado correctamente'
    toast.add({ severity: 'success', summary: 'Perfil actualizado', detail: 'Tus datos se han guardado correctamente', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al guardar el perfil', life: 3000 })
  } finally {
    guardando.value = false
  }
}

function validarContrasena() {
  erroresContrasena.value = {}
  if (!formularioContrasena.value.contrasena) {
    erroresContrasena.value.contrasena = 'La contraseña es obligatoria'
  } else if (formularioContrasena.value.contrasena.length < 6) {
    erroresContrasena.value.contrasena = 'La contraseña debe tener al menos 6 caracteres'
  }
  if (!formularioContrasena.value.confirmarContrasena) {
    erroresContrasena.value.confirmarContrasena = 'Confirma la nueva contraseña'
  } else if (formularioContrasena.value.contrasena !== formularioContrasena.value.confirmarContrasena) {
    erroresContrasena.value.confirmarContrasena = 'Las contraseñas no coinciden'
  }
  return Object.keys(erroresContrasena.value).length === 0
}

async function cambiarContrasena() {
  if (!validarContrasena()) return
  guardandoContrasena.value = true
  mensajeExitoContrasena.value = ''
  try {
    await api.put('/usuarios/perfil', { contrasena: formularioContrasena.value.contrasena })
    mensajeExitoContrasena.value = 'Contraseña cambiada correctamente'
    formularioContrasena.value = { contrasena: '', confirmarContrasena: '' }
    toast.add({ severity: 'success', summary: 'Contraseña actualizada', detail: 'Tu contraseña se ha cambiado correctamente', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: error.response?.data?.detail || 'Error al cambiar la contraseña', life: 3000 })
  } finally {
    guardandoContrasena.value = false
  }
}

onMounted(() => cargarDatosPerfil())
</script>