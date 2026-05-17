<!-- Componente raíz de la aplicación -->
<template>
  <div>
    <Toast />
    <ConfirmDialog />
    <RouterView v-slot="{ Component }">
      <Transition name="pagina" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </div>
</template>

<script setup>
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { RouterView } from 'vue-router'
</script>