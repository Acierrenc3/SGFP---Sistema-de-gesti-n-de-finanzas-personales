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
  // Europa
  { etiqueta: '🇪🇺 Euro (€)', valor: 'EUR' },
  { etiqueta: '🇬🇧 Libra esterlina (£)', valor: 'GBP' },
  { etiqueta: '🇨🇭 Franco suizo (CHF)', valor: 'CHF' },
  { etiqueta: '🇸🇪 Corona sueca (SEK)', valor: 'SEK' },
  { etiqueta: '🇳🇴 Corona noruega (NOK)', valor: 'NOK' },
  { etiqueta: '🇩🇰 Corona danesa (DKK)', valor: 'DKK' },
  { etiqueta: '🇵🇱 Esloti polaco (PLN)', valor: 'PLN' },
  { etiqueta: '🇨🇿 Corona checa (CZK)', valor: 'CZK' },
  { etiqueta: '🇭🇺 Forinto húngaro (HUF)', valor: 'HUF' },
  { etiqueta: '🇷🇴 Leu rumano (RON)', valor: 'RON' },
  // América
  { etiqueta: '🇺🇸 Dólar estadounidense ($)', valor: 'USD' },
  { etiqueta: '🇨🇦 Dólar canadiense (CA$)', valor: 'CAD' },
  { etiqueta: '🇲🇽 Peso mexicano (MX$)', valor: 'MXN' },
  { etiqueta: '🇧🇷 Real brasileño (R$)', valor: 'BRL' },
  { etiqueta: '🇦🇷 Peso argentino ($)', valor: 'ARS' },
  { etiqueta: '🇨🇱 Peso chileno ($)', valor: 'CLP' },
  { etiqueta: '🇨🇴 Peso colombiano ($)', valor: 'COP' },
  { etiqueta: '🇵🇪 Sol peruano (S/)', valor: 'PEN' },
  // Asia
  { etiqueta: '🇯🇵 Yen japonés (¥)', valor: 'JPY' },
  { etiqueta: '🇨🇳 Yuan chino (¥)', valor: 'CNY' },
  { etiqueta: '🇰🇷 Won surcoreano (₩)', valor: 'KRW' },
  { etiqueta: '🇮🇳 Rupia india (₹)', valor: 'INR' },
  { etiqueta: '🇸🇬 Dólar singapurense (S$)', valor: 'SGD' },
  { etiqueta: '🇭🇰 Dólar de Hong Kong (HK$)', valor: 'HKD' },
  { etiqueta: '🇹🇭 Baht tailandés (฿)', valor: 'THB' },
  { etiqueta: '🇦🇪 Dírham emiratí (د.إ)', valor: 'AED' },
  { etiqueta: '🇸🇦 Riyal saudí (﷼)', valor: 'SAR' },
  { etiqueta: '🇹🇷 Lira turca (₺)', valor: 'TRY' },
  // Oceanía
  { etiqueta: '🇦🇺 Dólar australiano (A$)', valor: 'AUD' },
  { etiqueta: '🇳🇿 Dólar neozelandés (NZ$)', valor: 'NZD' },
  // África
  { etiqueta: '🇿🇦 Rand sudafricano (R)', valor: 'ZAR' },
  { etiqueta: '🇪🇬 Libra egipcia (£)', valor: 'EGP' },
  // Cripto
  { etiqueta: '₿ Bitcoin (BTC)', valor: 'BTC' },
  { etiqueta: 'Ξ Ethereum (ETH)', valor: 'ETH' }
]

const zonasHorarias = [
  // España
  { etiqueta: '🇪🇸 Atlántico/Canarias (UTC+0/+1)', valor: 'Atlantic/Canary' },
  { etiqueta: '🇪🇸 Europa/Madrid (UTC+1/+2)', valor: 'Europe/Madrid' },
  // Europa
  { etiqueta: '🇬🇧 Europa/Londres (UTC+0/+1)', valor: 'Europe/London' },
  { etiqueta: '🇫🇷 Europa/París (UTC+1/+2)', valor: 'Europe/Paris' },
  { etiqueta: '🇩🇪 Europa/Berlín (UTC+1/+2)', valor: 'Europe/Berlin' },
  { etiqueta: '🇮🇹 Europa/Roma (UTC+1/+2)', valor: 'Europe/Rome' },
  { etiqueta: '🇵🇹 Europa/Lisboa (UTC+0/+1)', valor: 'Europe/Lisbon' },
  { etiqueta: '🇳🇱 Europa/Ámsterdam (UTC+1/+2)', valor: 'Europe/Amsterdam' },
  { etiqueta: '🇧🇪 Europa/Bruselas (UTC+1/+2)', valor: 'Europe/Brussels' },
  { etiqueta: '🇨🇭 Europa/Zúrich (UTC+1/+2)', valor: 'Europe/Zurich' },
  { etiqueta: '🇸🇪 Europa/Estocolmo (UTC+1/+2)', valor: 'Europe/Stockholm' },
  { etiqueta: '🇳🇴 Europa/Oslo (UTC+1/+2)', valor: 'Europe/Oslo' },
  { etiqueta: '🇩🇰 Europa/Copenhague (UTC+1/+2)', valor: 'Europe/Copenhagen' },
  { etiqueta: '🇫🇮 Europa/Helsinki (UTC+2/+3)', valor: 'Europe/Helsinki' },
  { etiqueta: '🇵🇱 Europa/Varsovia (UTC+1/+2)', valor: 'Europe/Warsaw' },
  { etiqueta: '🇷🇴 Europa/Bucarest (UTC+2/+3)', valor: 'Europe/Bucharest' },
  { etiqueta: '🇬🇷 Europa/Atenas (UTC+2/+3)', valor: 'Europe/Athens' },
  { etiqueta: '🇷🇺 Europa/Moscú (UTC+3)', valor: 'Europe/Moscow' },
  // América
  { etiqueta: '🇺🇸 América/Nueva York (UTC-5/-4)', valor: 'America/New_York' },
  { etiqueta: '🇺🇸 América/Chicago (UTC-6/-5)', valor: 'America/Chicago' },
  { etiqueta: '🇺🇸 América/Denver (UTC-7/-6)', valor: 'America/Denver' },
  { etiqueta: '🇺🇸 América/Los Ángeles (UTC-8/-7)', valor: 'America/Los_Angeles' },
  { etiqueta: '🇨🇦 América/Toronto (UTC-5/-4)', valor: 'America/Toronto' },
  { etiqueta: '🇲🇽 América/Ciudad de México (UTC-6/-5)', valor: 'America/Mexico_City' },
  { etiqueta: '🇧🇷 América/São Paulo (UTC-3)', valor: 'America/Sao_Paulo' },
  { etiqueta: '🇦🇷 América/Buenos Aires (UTC-3)', valor: 'America/Argentina/Buenos_Aires' },
  { etiqueta: '🇨🇱 América/Santiago (UTC-4/-3)', valor: 'America/Santiago' },
  { etiqueta: '🇨🇴 América/Bogotá (UTC-5)', valor: 'America/Bogota' },
  { etiqueta: '🇵🇪 América/Lima (UTC-5)', valor: 'America/Lima' },
  // Asia
  { etiqueta: '🇯🇵 Asia/Tokio (UTC+9)', valor: 'Asia/Tokyo' },
  { etiqueta: '🇨🇳 Asia/Shanghái (UTC+8)', valor: 'Asia/Shanghai' },
  { etiqueta: '🇰🇷 Asia/Seúl (UTC+9)', valor: 'Asia/Seoul' },
  { etiqueta: '🇮🇳 Asia/Calcuta (UTC+5:30)', valor: 'Asia/Calcutta' },
  { etiqueta: '🇸🇬 Asia/Singapur (UTC+8)', valor: 'Asia/Singapore' },
  { etiqueta: '🇦🇪 Asia/Dubái (UTC+4)', valor: 'Asia/Dubai' },
  { etiqueta: '🇹🇷 Europa/Estambul (UTC+3)', valor: 'Europe/Istanbul' },
  // Oceanía
  { etiqueta: '🇦🇺 Australia/Sídney (UTC+10/+11)', valor: 'Australia/Sydney' },
  { etiqueta: '🇦🇺 Australia/Melbourne (UTC+10/+11)', valor: 'Australia/Melbourne' },
  { etiqueta: '🇳🇿 Pacífico/Auckland (UTC+12/+13)', valor: 'Pacific/Auckland' },
  // África
  { etiqueta: '🇿🇦 África/Johannesburgo (UTC+2)', valor: 'Africa/Johannesburg' },
  { etiqueta: '🇪🇬 África/El Cairo (UTC+2)', valor: 'Africa/Cairo' },
  { etiqueta: '🇳🇬 África/Lagos (UTC+1)', valor: 'Africa/Lagos' }
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