<!-- Vista de inicio de sesión -->
<!-- Basado en: https://primevue.org/inputtext/ -->

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-md">
      <!-- Tarjeta de inicio de sesión -->
      <Card>
        <template #header>
          <div class="text-center pt-6">
            <h1 class="text-3xl font-bold text-primary-600">SGFP</h1>
            <p class="text-gray-500 mt-1">Sistema de Gestión de Finanzas Personales</p>
          </div>
        </template>

        <template #content>
          <form @submit.prevent="enviarFormulario" class="flex flex-col gap-4">
            <!-- Campo email -->
            <div class="flex flex-col gap-1">
              <label for="email" class="font-medium">Email</label>
              <InputText
                id="email"
                v-model="formulario.email"
                type="email"
                placeholder="tu@email.com"
                :invalid="!!errores.email"
                fluid
              />
              <small class="text-red-500" v-if="errores.email">{{ errores.email }}</small>
            </div>

            <!-- Campo contraseña -->
            <div class="flex flex-col gap-1">
              <label for="contrasena" class="font-medium">Contraseña</label>
              <Password
                id="contrasena"
                v-model="formulario.contrasena"
                placeholder="Tu contraseña"
                :feedback="false"
                :invalid="!!errores.contrasena"
                fluid
                toggleMask
              />
              <small class="text-red-500" v-if="errores.contrasena">{{ errores.contrasena }}</small>
            </div>

            <!-- Mensaje de error general -->
            <Message v-if="errorGeneral" severity="error">{{ errorGeneral }}</Message>

            <!-- Botón de envío -->
            <Button
              type="submit"
              label="Iniciar sesión"
              :loading="cargando"
              fluid
            />
          </form>
        </template>

        <template #footer>
          <div class="text-center pb-4">
            <span class="text-gray-500">¿No tienes cuenta? </span>
            <RouterLink to="/registro" class="text-primary-600 font-medium hover:underline">
              Regístrate
            </RouterLink>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'
import { RouterLink } from 'vue-router'
import { useAutenticacionStore } from '../stores/autenticacion'

const enrutador = useRouter()
const toast = useToast()
const autenticacion = useAutenticacionStore()

// Estado del formulario
const formulario = ref({
  email: '',
  contrasena: ''
})

const errores = ref({})
const errorGeneral = ref('')
const cargando = ref(false)

// Valida el formulario antes de enviar
function validar() {
  errores.value = {}

  if (!formulario.value.email) {
    errores.value.email = 'El email es obligatorio'
  }
  if (!formulario.value.contrasena) {
    errores.value.contrasena = 'La contraseña es obligatoria'
  }

  return Object.keys(errores.value).length === 0
}

async function enviarFormulario() {
  if (!validar()) return

  cargando.value = true
  errorGeneral.value = ''

  try {
    await autenticacion.iniciarSesion(
      formulario.value.email,
      formulario.value.contrasena
    )

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