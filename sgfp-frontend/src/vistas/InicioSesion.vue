<!-- Vista de inicio de sesión con estilo Glassmorphism -->

<template>
  <div class="min-h-screen flex items-center justify-center p-4" style="background: var(--gradiente-fondo)">
    <!-- Círculos decorativos de fondo -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-96 h-96 rounded-full opacity-20"
        style="background: radial-gradient(circle, #e040fb, transparent)" />
      <div class="absolute -bottom-40 -left-40 w-96 h-96 rounded-full opacity-20"
        style="background: radial-gradient(circle, #00b4d8, transparent)" />
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full opacity-10"
        style="background: radial-gradient(circle, #7c3aed, transparent)" />
    </div>

    <!-- Tarjeta glass -->
    <div class="glass w-full max-w-md p-8 relative z-10">
    <!-- Logo -->
    <div class="flex flex-col items-center mb-8">
      <img
        src="/logo.png"
        alt="SGFP Logo"
        class="w-20 h-20 rounded-2xl object-cover mb-3"
      />
      <h1 class="text-3xl font-bold texto-glass">SGFP</h1>
      <p class="texto-glass-suave text-sm mt-1 text-center">Sistema de Gestión de Finanzas Personales</p>
    </div>

      <!-- Formulario -->
      <form @submit.prevent="enviarFormulario" class="flex flex-col gap-5">
        <!-- Email -->
        <div class="flex flex-col gap-2">
          <label class="texto-glass text-sm font-medium">Email</label>
          <div class="relative">
            <i class="pi pi-envelope absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave" />
            <input
              v-model="formulario.email"
              type="email"
              placeholder="tu@email.com"
              class="w-full pl-10 pr-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);"
              :class="errores.email ? 'border-red-400' : 'focus:border-purple-400'"
            />
          </div>
          <small class="text-red-400" v-if="errores.email">{{ errores.email }}</small>
        </div>

        <!-- Contraseña -->
        <div class="flex flex-col gap-2">
          <label class="texto-glass text-sm font-medium">Contraseña</label>
          <div class="relative">
            <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave" />
            <input
              v-model="formulario.contrasena"
              :type="mostrarContrasena ? 'text' : 'password'"
              placeholder="Tu contraseña"
              class="w-full pl-10 pr-10 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);"
              :class="errores.contrasena ? 'border-red-400' : 'focus:border-purple-400'"
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 texto-glass-suave hover:text-white transition-colors"
              @click="mostrarContrasena = !mostrarContrasena"
            >
              <i :class="mostrarContrasena ? 'pi pi-eye-slash' : 'pi pi-eye'" />
            </button>
          </div>
          <small class="text-red-400" v-if="errores.contrasena">{{ errores.contrasena }}</small>
        </div>

        <!-- Error general -->
        <div
          v-if="errorGeneral"
          class="flex items-center gap-2 px-4 py-3 rounded-xl text-red-300 text-sm"
          style="background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3)"
        >
          <i class="pi pi-exclamation-circle" />
          {{ errorGeneral }}
        </div>

        <!-- Botón -->
        <button
          type="submit"
          :disabled="cargando"
          class="w-full py-3 rounded-xl font-semibold text-white transition-all hover:opacity-90 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <span v-if="!cargando">Iniciar sesión</span>
          <i v-else class="pi pi-spin pi-spinner" />
        </button>
      </form>

      <!-- Enlace registro -->
      <p class="text-center mt-6 texto-glass-suave text-sm">
        ¿No tienes cuenta?
        <RouterLink to="/registro" class="text-purple-400 hover:text-purple-300 font-medium ml-1 transition-colors">
          Regístrate
        </RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { RouterLink } from 'vue-router'
import { useAutenticacionStore } from '../stores/autenticacion'

const enrutador = useRouter()
const toast = useToast()
const autenticacion = useAutenticacionStore()

const formulario = ref({ email: '', contrasena: '' })
const errores = ref({})
const errorGeneral = ref('')
const cargando = ref(false)
const mostrarContrasena = ref(false)

function validar() {
  errores.value = {}
  if (!formulario.value.email) errores.value.email = 'El email es obligatorio'
  if (!formulario.value.contrasena) errores.value.contrasena = 'La contraseña es obligatoria'
  return Object.keys(errores.value).length === 0
}

async function enviarFormulario() {
  if (!validar()) return
  cargando.value = true
  errorGeneral.value = ''

  try {
    await autenticacion.iniciarSesion(formulario.value.email, formulario.value.contrasena)
    toast.add({
      severity: 'success',
      summary: 'Bienvenido',
      detail: 'Sesión iniciada correctamente',
      life: 3000
    })
    enrutador.push({ name: 'Dashboard' })
  } catch (error) {
    errorGeneral.value = error.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    cargando.value = false
  }
}
</script>