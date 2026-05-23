<!-- Vista de registro con estilo Glassmorphism -->

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
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-4"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)">
          <i class="pi pi-user-plus text-white text-2xl" />
        </div>
        <h1 class="text-3xl font-bold texto-glass">Crear cuenta</h1>
        <p class="texto-glass-suave mt-1">Empieza a gestionar tus finanzas</p>
      </div>

      <!-- Formulario -->
      <form @submit.prevent="enviarFormulario" class="flex flex-col gap-5">
        <!-- Nombre -->
        <div class="flex flex-col gap-2">
          <label class="texto-glass text-sm font-medium">Nombre</label>
          <div class="relative">
            <i class="pi pi-user absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave" />
            <input
              v-model="formulario.nombre"
              type="text"
              placeholder="Tu nombre"
              class="w-full pl-10 pr-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
              :class="errores.nombre ? 'border-red-400' : 'focus:border-purple-400'"
            />
          </div>
          <small class="text-red-400" v-if="errores.nombre">{{ errores.nombre }}</small>
        </div>

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
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
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
              placeholder="Mínimo 6 caracteres"
              class="w-full pl-10 pr-10 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
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

          <!-- Indicador fortaleza -->
          <div v-if="formulario.contrasena" class="flex flex-col gap-1">
            <div class="flex gap-1">
              <div
                v-for="n in 4"
                :key="n"
                class="h-1 flex-1 rounded-full transition-all duration-300"
                :style="n <= nivelFortaleza
                  ? `background: ${colorFortaleza}`
                  : 'background: rgba(255,255,255,0.1)'"
              />
            </div>
            <p class="text-xs transition-all" :style="`color: ${colorFortaleza}`">
              {{ textoFortaleza }}
            </p>
          </div>

          <!-- Requisitos -->
          <div class="flex flex-col gap-1 mt-1">
            <div class="flex items-center gap-2">
              <i
                class="text-xs"
                :class="formulario.contrasena.length >= 6 ? 'pi pi-check-circle text-green-400' : 'pi pi-circle texto-glass-suave'"
              />
              <span class="text-xs texto-glass-suave">Mínimo 6 caracteres</span>
            </div>
            <div class="flex items-center gap-2">
              <i
                class="text-xs"
                :class="/[a-zA-Z]/.test(formulario.contrasena) && /[0-9]/.test(formulario.contrasena) ? 'pi pi-check-circle text-green-400' : 'pi pi-circle texto-glass-suave'"
              />
              <span class="text-xs texto-glass-suave">Al menos una letra y un número</span>
            </div>
            <div class="flex items-center gap-2">
              <i
                class="text-xs"
                :class="/[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]/.test(formulario.contrasena) ? 'pi pi-check-circle text-green-400' : 'pi pi-circle texto-glass-suave'"
              />
              <span class="text-xs texto-glass-suave">Al menos un carácter especial (!@#$...)</span>
            </div>
          </div>

          <small class="text-red-400" v-if="errores.contrasena">{{ errores.contrasena }}</small>
        </div>

        <!-- Confirmar contraseña -->
        <div class="flex flex-col gap-2">
          <label class="texto-glass text-sm font-medium">Confirmar contraseña</label>
          <div class="relative">
            <i class="pi pi-lock absolute left-3 top-1/2 -translate-y-1/2 texto-glass-suave" />
            <input
              v-model="formulario.confirmarContrasena"
              :type="mostrarConfirmar ? 'text' : 'password'"
              placeholder="Repite tu contraseña"
              class="w-full pl-10 pr-10 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
              :class="errores.confirmarContrasena ? 'border-red-400' : 'focus:border-purple-400'"
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 texto-glass-suave hover:text-white transition-colors"
              @click="mostrarConfirmar = !mostrarConfirmar"
            >
              <i :class="mostrarConfirmar ? 'pi pi-eye-slash' : 'pi pi-eye'" />
            </button>
          </div>
          <small class="text-red-400" v-if="errores.confirmarContrasena">{{ errores.confirmarContrasena }}</small>
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
          <span v-if="!cargando">Crear cuenta</span>
          <i v-else class="pi pi-spin pi-spinner" />
        </button>
      </form>

      <!-- Enlace login -->
      <p class="text-center mt-6 texto-glass-suave text-sm">
        ¿Ya tienes cuenta?
        <RouterLink to="/inicio-sesion" class="text-purple-400 hover:text-purple-300 font-medium ml-1 transition-colors">
          Inicia sesión
        </RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { RouterLink } from 'vue-router'
import { useAutenticacionStore } from '../stores/autenticacion'

const enrutador = useRouter()
const toast = useToast()
const autenticacion = useAutenticacionStore()

const formulario = ref({ nombre: '', email: '', contrasena: '', confirmarContrasena: '' })
const errores = ref({})
const errorGeneral = ref('')
const cargando = ref(false)
const mostrarContrasena = ref(false)
const mostrarConfirmar = ref(false)

const nivelFortaleza = computed(() => {
  const c = formulario.value.contrasena
  if (!c) return 0
  let nivel = 0
  if (c.length >= 6) nivel++
  if (/[a-zA-Z]/.test(c) && /[0-9]/.test(c)) nivel++
  if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(c)) nivel++
  if (c.length >= 10) nivel++
  return nivel
})

const colorFortaleza = computed(() => {
  if (nivelFortaleza.value <= 1) return '#ef4444'
  if (nivelFortaleza.value === 2) return '#f59e0b'
  if (nivelFortaleza.value === 3) return '#10b981'
  return '#7c3aed'
})

const textoFortaleza = computed(() => {
  if (nivelFortaleza.value <= 1) return 'Contraseña débil'
  if (nivelFortaleza.value === 2) return 'Contraseña aceptable'
  if (nivelFortaleza.value === 3) return 'Contraseña fuerte'
  return 'Contraseña muy fuerte'
})

function validar() {
  errores.value = {}

  if (!formulario.value.nombre.trim()) {
    errores.value.nombre = 'El nombre es obligatorio'
  } else if (formulario.value.nombre.trim().length < 2) {
    errores.value.nombre = 'El nombre debe tener al menos 2 caracteres'
  }

  const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!formulario.value.email) {
    errores.value.email = 'El email es obligatorio'
  } else if (!regexEmail.test(formulario.value.email)) {
    errores.value.email = 'Introduce un email válido'
  }

  const contrasena = formulario.value.contrasena
  if (!contrasena) {
    errores.value.contrasena = 'La contraseña es obligatoria'
  } else if (contrasena.length < 6) {
    errores.value.contrasena = 'La contraseña debe tener al menos 6 caracteres'
  } else if (!/[a-zA-Z]/.test(contrasena)) {
    errores.value.contrasena = 'La contraseña debe contener al menos una letra'
  } else if (!/[0-9]/.test(contrasena)) {
    errores.value.contrasena = 'La contraseña debe contener al menos un número'
  } else if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(contrasena)) {
    errores.value.contrasena = 'La contraseña debe contener al menos un carácter especial (!@#$...)'
  }

  if (!formulario.value.confirmarContrasena) {
    errores.value.confirmarContrasena = 'Confirma tu contraseña'
  } else if (formulario.value.contrasena !== formulario.value.confirmarContrasena) {
    errores.value.confirmarContrasena = 'Las contraseñas no coinciden'
  }

  return Object.keys(errores.value).length === 0
}

async function enviarFormulario() {
  if (!validar()) return
  cargando.value = true
  errorGeneral.value = ''

  try {
    await autenticacion.registrar(formulario.value.nombre, formulario.value.email, formulario.value.contrasena)
    toast.add({ severity: 'success', summary: 'Cuenta creada', detail: 'Tu cuenta se ha creado correctamente', life: 3000 })
    enrutador.push({ name: 'InicioSesion' })
  } catch (error) {
    errorGeneral.value = error.response?.data?.detail || 'Error al crear la cuenta'
  } finally {
    cargando.value = false
  }
}
</script>