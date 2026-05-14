<!-- Componente raíz de la aplicación -->
<!-- Basado en: https://vuejs.org/guide/essentials/application.html -->

<template>
  <div>
    <!-- Componente de notificaciones globales de PrimeVue -->
    <Toast />
    <!-- Componente de confirmación global de PrimeVue -->
    <ConfirmDialog />
    <!-- Vista actual según la ruta -->
    <RouterView />
  </div>
</template>

<script setup>
// Basado en: https://primevue.org/toast/
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { RouterView } from 'vue-router'
</script>