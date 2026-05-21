<!-- Vista 404 - Página no encontrada -->

<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-6 text-center"
    style="background: var(--gradiente-fondo)">

    <!-- Círculos decorativos -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-96 h-96 rounded-full opacity-20"
        style="background: radial-gradient(circle, #e040fb, transparent)" />
      <div class="absolute -bottom-40 -left-40 w-96 h-96 rounded-full opacity-20"
        style="background: radial-gradient(circle, #00b4d8, transparent)" />
    </div>

    <div class="relative z-10 animar-entrada">
      <!-- Logo -->
      <img src="/logo.png" alt="SGFP" class="w-20 h-20 rounded-2xl object-cover mx-auto mb-8"
        style="box-shadow: 0 8px 32px rgba(124,58,237,0.3)" />

      <!-- Número 404 -->
      <h1 class="text-8xl md:text-9xl font-bold mb-4 texto-gradiente">404</h1>

      <!-- Mensaje -->
      <h2 class="text-2xl md:text-3xl font-bold texto-glass mb-4">
        Página no encontrada
      </h2>
      <p class="texto-glass-suave text-lg max-w-md mx-auto mb-10">
        La página que buscas no existe o ha sido movida.
      </p>

      <!-- Botones -->
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <RouterLink
          to="/dashboard"
          class="px-8 py-3 rounded-xl text-white font-semibold transition-all hover:opacity-90 active:scale-95"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <i class="pi pi-home mr-2" />
          Ir al Dashboard
        </RouterLink>
        <button
          @click="enrutador.back()"
          class="px-8 py-3 rounded-xl text-sm font-medium transition-all hover:text-white texto-glass-suave"
          style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
        >
          <i class="pi pi-arrow-left mr-2" />
          Volver atrás
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'

const enrutador = useRouter()
</script>