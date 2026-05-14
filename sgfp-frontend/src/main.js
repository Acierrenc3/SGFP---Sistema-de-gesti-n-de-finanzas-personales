// Punto de entrada principal de la aplicación Vue
// Basado en:
// https://primevue.org/installation/
// https://pinia.vuejs.org/getting-started.html
// https://router.vuejs.org/installation.html

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import 'primeicons/primeicons.css'

import App from './App.vue'
import enrutador from './enrutador'
import './style.css'

const app = createApp(App)

// Configura Pinia como gestor de estado global
app.use(createPinia())

// Configura Vue Router
app.use(enrutador)

// Configura PrimeVue con el tema Aura
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            // Prefijo de las variables CSS de PrimeVue
            cssLayer: {
                name: 'primevue',
                order: 'tailwind-base, primevue, tailwind-utilities'
            }
        }
    }
})

// Servicios globales de PrimeVue
app.use(ToastService)
app.use(ConfirmationService)

app.mount('#app')