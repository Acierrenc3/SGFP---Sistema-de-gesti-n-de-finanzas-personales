<!-- Vista del perfil del usuario -->
<!-- Basado en: https://primevue.org/inputtext/ -->

<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Perfil</h2>
        <p class="text-gray-500">Gestiona tu información personal</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Tarjeta de información personal -->
        <Card>
          <template #title>Información personal</template>
          <template #content>
            <form @submit.prevent="guardarPerfil" class="flex flex-col gap-4">
              <!-- Avatar -->
              <div class="flex justify-center mb-2">
                <Avatar
                  :label="inicialUsuario"
                  shape="circle"
                  size="xlarge"
                  class="bg-primary-100 text-primary-600 text-3xl"
                />
              </div>

              <!-- Nombre -->
              <div class="flex flex-col gap-1">
                <label class="font-medium">Nombre</label>
                <InputText
                  v-model="formulario.nombre"
                  placeholder="Tu nombre"
                  :invalid="!!errores.nombre"
                  fluid
                />
                <small class="text-red-500" v-if="errores.nombre">{{ errores.nombre }}</small>
              </div>

              <!-- Email (solo lectura) -->
              <div class="flex flex-col gap-1">
                <label class="font-medium">Email</label>
                <InputText
                  :value="autenticacion.usuario?.email"
                  disabled
                  fluid
                />
                <small class="text-gray-400">El email no se puede modificar</small>
              </div>

              <!-- Moneda -->
              <div class="flex flex-col gap-1">
                <label class="font-medium">Moneda</label>
                <Select
                  v-model="formulario.moneda"
                  :options="monedas"
                  optionLabel="etiqueta"
                  optionValue="valor"
                  placeholder="Selecciona una moneda"
                  fluid
                />
              </div>

              <!-- Zona horaria -->
              <div class="flex flex-col gap-1">
                <label class="font-medium">Zona horaria</label>
                <Select
                  v-model="formulario.zona_horaria"
                  :options="zonasHorarias"
                  optionLabel="etiqueta"
                  optionValue="valor"
                  placeholder="Selecciona una zona horaria"
                  fluid
                />
              </div>

              <!-- Mensaje de éxito -->
              <Message v-if="mensajeExito" severity="success">{{ mensajeExito }}</Message>

              <!-- Botón guardar -->
              <Button
                type="submit"
                label="Guardar cambios"
                icon="pi pi-save"
                :loading="guardando"
                fluid
              />
            </form>
          </template>
        </Card>

        <!-- Tarjeta de cambio de contraseña -->
        <Card>
          <template #title>Cambiar contraseña</template>
          <template #content>
            <form @submit.prevent="cambiarContrasena" class="flex flex-col gap-4">
              <!-- Nueva contraseña -->
              <div class="flex flex-col gap-1">
                <label class="font-medium">Nueva contraseña</label>
                <Password
                  v-model="formularioContrasena.contrasena"
                  placeholder="Mínimo 6 caracteres"
                  :invalid="!!erroresContrasena.contrasena"
                  fluid
                  toggleMask
                />
                <small class="text-red-500" v-if="erroresContrasena.contrasena">
                  {{ erroresContrasena.contrasena }}
                </small>
              </div>

              <!-- Confirmar nueva contraseña -->
              <div class="flex flex-col gap-1">
                <label class="font-medium">Confirmar nueva contraseña</label>
                <Password
                  v-model="formularioContrasena.confirmarContrasena"
                  placeholder="Repite la nueva contraseña"
                  :feedback="false"
                  :invalid="!!erroresContrasena.confirmarContrasena"
                  fluid
                  toggleMask
                />
                <small class="text-red-500" v-if="erroresContrasena.confirmarContrasena">
                  {{ erroresContrasena.confirmarContrasena }}
                </small>
              </div>

              <!-- Mensaje de éxito -->
              <Message v-if="mensajeExitoContrasena" severity="success">
                {{ mensajeExitoContrasena }}
              </Message>

              <!-- Botón guardar -->
              <Button
                type="submit"
                label="Cambiar contraseña"
                icon="pi pi-lock"
                severity="secondary"
                :loading="guardandoContrasena"
                fluid
              />
            </form>
          </template>
        </Card>
      </div>
    </div>
  </LayoutPrincipal>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Select from 'primevue/select'
import Avatar from 'primevue/avatar'
import Message from 'primevue/message'
import LayoutPrincipal from '../componentes/LayoutPrincipal.vue'
import { useAutenticacionStore } from '../stores/autenticacion'
import api from '../servicios/api'

const toast = useToast()
const autenticacion = useAutenticacionStore()

// Estado
const guardando = ref(false)
const guardandoContrasena = ref(false)
const errores = ref({})
const erroresContrasena = ref({})
const mensajeExito = ref('')
const mensajeExitoContrasena = ref('')

// Formulario de perfil
const formulario = ref({
  nombre: '',
  moneda: 'EUR',
  zona_horaria: 'Europe/Madrid'
})

// Formulario de contraseña
const formularioContrasena = ref({
  contrasena: '',
  confirmarContrasena: ''
})

// Opciones de moneda
const monedas = [
  { etiqueta: 'Euro (€)', valor: 'EUR' },
  { etiqueta: 'Dólar ($)', valor: 'USD' },
  { etiqueta: 'Libra (£)', valor: 'GBP' },
  { etiqueta: 'Franco suizo (CHF)', valor: 'CHF' }
]

// Opciones de zona horaria
const zonasHorarias = [
  { etiqueta: 'Europa/Madrid', valor: 'Europe/Madrid' },
  { etiqueta: 'Europa/Londres', valor: 'Europe/London' },
  { etiqueta: 'Europa/París', valor: 'Europe/Paris' },
  { etiqueta: 'América/Nueva York', valor: 'America/New_York' },
  { etiqueta: 'América/Los Ángeles', valor: 'America/Los_Angeles' }
]

// Inicial del nombre para el avatar
const inicialUsuario = computed(() => {
  return autenticacion.usuario?.nombre?.charAt(0).toUpperCase() || 'U'
})

// Carga los datos del perfil en el formulario
function cargarDatosPerfil() {
  if (autenticacion.usuario) {
    formulario.value = {
      nombre: autenticacion.usuario.nombre,
      moneda: autenticacion.usuario.moneda,
      zona_horaria: autenticacion.usuario.zona_horaria
    }
  }
}

// Valida el formulario de perfil
function validar() {
  errores.value = {}
  if (!formulario.value.nombre) errores.value.nombre = 'El nombre es obligatorio'
  return Object.keys(errores.value).length === 0
}

// Guarda los cambios del perfil
async function guardarPerfil() {
  if (!validar()) return
  guardando.value = true
  mensajeExito.value = ''

  try {
    await api.put('/usuarios/perfil', formulario.value)
    await autenticacion.obtenerPerfil()

    mensajeExito.value = 'Perfil actualizado correctamente'
    toast.add({
      severity: 'success',
      summary: 'Perfil actualizado',
      detail: 'Tus datos se han guardado correctamente',
      life: 3000
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.response?.data?.detail || 'Error al guardar el perfil',
      life: 3000
    })
  } finally {
    guardando.value = false
  }
}

// Valida el formulario de contraseña
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

// Cambia la contraseña del usuario
async function cambiarContrasena() {
  if (!validarContrasena()) return
  guardandoContrasena.value = true
  mensajeExitoContrasena.value = ''

  try {
    await api.put('/usuarios/perfil', {
      contrasena: formularioContrasena.value.contrasena
    })

    mensajeExitoContrasena.value = 'Contraseña cambiada correctamente'
    formularioContrasena.value = { contrasena: '', confirmarContrasena: '' }

    toast.add({
      severity: 'success',
      summary: 'Contraseña actualizada',
      detail: 'Tu contraseña se ha cambiado correctamente',
      life: 3000
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.response?.data?.detail || 'Error al cambiar la contraseña',
      life: 3000
    })
  } finally {
    guardandoContrasena.value = false
  }
}

onMounted(() => cargarDatosPerfil())
</script>