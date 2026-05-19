<!-- Landing Page de SGFP -->

<template>
  <div style="background: var(--gradiente-fondo)" class="min-h-screen">

    <!-- Círculos decorativos globales -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-96 h-96 rounded-full opacity-20"
        style="background: radial-gradient(circle, #e040fb, transparent)" />
      <div class="absolute -bottom-40 -left-40 w-96 h-96 rounded-full opacity-20"
        style="background: radial-gradient(circle, #00b4d8, transparent)" />
      <div class="absolute top-1/2 left-1/4 w-64 h-64 rounded-full opacity-10"
        style="background: radial-gradient(circle, #7c3aed, transparent)" />
    </div>

    <!-- NAVBAR -->
    <nav
      class="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4"
      style="background: rgba(26,26,46,0.85); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,0.08)"
    >
      <div class="flex items-center gap-3">
        <img src="/logo.png" alt="SGFP" class="w-9 h-9 rounded-xl object-cover" />
        <span class="font-bold texto-glass text-lg">SGFP</span>
      </div>

      <div class="hidden md:flex items-center gap-8">
        <button @click="scrollTo('#features')" class="texto-glass-suave text-sm hover:text-white transition-colors">Características</button>
        <button @click="scrollTo('#como-funciona')" class="texto-glass-suave text-sm hover:text-white transition-colors">Cómo funciona</button>
        <button @click="scrollTo('#precios')" class="texto-glass-suave text-sm hover:text-white transition-colors">Precios</button>
      </div>

      <div class="flex items-center gap-3">
        <RouterLink
          to="/inicio-sesion"
          class="texto-glass-suave text-sm hover:text-white transition-colors hidden md:block"
        >
          Iniciar sesión
        </RouterLink>
        <RouterLink
          to="/registro"
          class="px-4 py-2 rounded-xl text-white text-sm font-medium transition-all hover:opacity-90"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          Empezar gratis
        </RouterLink>
      </div>
    </nav>

    <!-- SECCIÓN 1: HERO -->
    <section class="relative z-10 flex flex-col items-center justify-center min-h-screen text-center px-6 pt-20">
      <div class="animar-entrada">
        <div
          class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium mb-8"
          style="background: rgba(124,58,237,0.2); border: 1px solid rgba(124,58,237,0.4); color: #a78bfa"
        >
          <i class="pi pi-star-fill text-xs" />
          Gestión de finanzas personales simple y potente
        </div>

        <h1 class="text-4xl md:text-6xl font-bold texto-glass mb-6 leading-tight">
          Toma el control de<br />
          <span class="texto-gradiente">tus finanzas</span>
        </h1>

        <p class="texto-glass-suave text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
          SGFP te ayuda a registrar ingresos y gastos, controlar presupuestos,
          automatizar transacciones recurrentes y visualizar tu situación financiera en tiempo real.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <RouterLink
            to="/registro"
            class="px-8 py-4 rounded-2xl text-white font-semibold text-lg transition-all hover:opacity-90 active:scale-95"
            style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
          >
            Empezar gratis
            <i class="pi pi-arrow-right ml-2" />
          </RouterLink>
          <button
            @click="scrollTo('#features')"
            class="px-8 py-4 rounded-2xl text-sm font-medium transition-all hover:text-white texto-glass-suave"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            Ver características
          </button>
        </div>
      </div>

      <!-- Preview app -->
      <div class="mt-16 w-full max-w-4xl animar-entrada">
        <div class="glass p-6 rounded-2xl" style="box-shadow: 0 32px 64px rgba(0,0,0,0.4)">
          <div class="grid grid-cols-3 gap-3 mb-4">
            <div class="glass p-4 rounded-xl">
              <p class="texto-glass-suave text-xs mb-1">Ingresos</p>
              <p class="text-green-400 font-bold text-lg">2.450,00 €</p>
            </div>
            <div class="glass p-4 rounded-xl">
              <p class="texto-glass-suave text-xs mb-1">Gastos</p>
              <p class="text-red-400 font-bold text-lg">1.230,00 €</p>
            </div>
            <div class="glass p-4 rounded-xl">
              <p class="texto-glass-suave text-xs mb-1">Balance</p>
              <p class="text-purple-400 font-bold text-lg">1.220,00 €</p>
            </div>
          </div>
          <div class="glass p-4 rounded-xl">
            <div class="flex justify-between mb-2">
              <span class="texto-glass text-xs font-medium">Alimentación</span>
              <span class="texto-glass-suave text-xs">240 € / 300 €</span>
            </div>
            <div class="w-full h-2 rounded-full" style="background: rgba(255,255,255,0.1)">
              <div class="h-2 rounded-full w-4/5" style="background: linear-gradient(90deg, #f59e0b, #d97706)" />
            </div>
            <div class="flex justify-between mb-2 mt-3">
              <span class="texto-glass text-xs font-medium">Transporte</span>
              <span class="texto-glass-suave text-xs">45 € / 150 €</span>
            </div>
            <div class="w-full h-2 rounded-full" style="background: rgba(255,255,255,0.1)">
              <div class="h-2 rounded-full w-1/4" style="background: linear-gradient(90deg, #7c3aed, #00b4d8)" />
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="mt-12 flex flex-col items-center gap-2 texto-glass-suave animate-bounce">
        <span class="text-xs">Descubre más</span>
        <i class="pi pi-chevron-down" />
      </div>
    </section>

<!-- SECCIÓN 2: FEATURES -->
<section id="features" class="relative z-10 py-24 px-6">
  <div class="max-w-6xl mx-auto">
    <div class="text-center mb-16 scroll-oculto">
      <h2 class="text-3xl md:text-4xl font-bold texto-glass mb-4">
        Todo lo que necesitas para
        <span class="texto-gradiente">gestionar tu dinero</span>
      </h2>
      <p class="texto-glass-suave text-lg max-w-2xl mx-auto">
        SGFP combina simplicidad y potencia para darte el control total de tus finanzas personales.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="(feature, index) in features"
        :key="feature.titulo"
        class="glass p-6 hover:scale-105 transition-transform duration-300 scroll-oculto"
        :class="`delay-${index + 1}`"
      >
        <div
          class="w-12 h-12 rounded-xl flex items-center justify-center mb-4"
          :style="`background: ${feature.color}20; border: 1px solid ${feature.color}40`"
        >
          <i :class="feature.icono" :style="`color: ${feature.color}; font-size: 1.3rem`" />
        </div>
        <h3 class="texto-glass font-semibold text-lg mb-2">{{ feature.titulo }}</h3>
        <p class="texto-glass-suave text-sm leading-relaxed">{{ feature.descripcion }}</p>
      </div>
    </div>
  </div>
</section>

<!-- SECCIÓN 3: CÓMO FUNCIONA -->
<section id="como-funciona" class="relative z-10 py-24 px-6">
  <div class="max-w-4xl mx-auto">
    <div class="text-center mb-16 scroll-oculto">
      <h2 class="text-3xl md:text-4xl font-bold texto-glass mb-4">
        Empieza en
        <span class="texto-gradiente">3 simples pasos</span>
      </h2>
      <p class="texto-glass-suave text-lg">Sin complicaciones, sin tarjeta de crédito.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div
        v-for="(paso, index) in pasos"
        :key="paso.titulo"
        class="glass p-6 text-center relative scroll-oculto-escala"
        :class="`delay-${index + 1}`"
      >
        <div
          class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-bold text-white mx-auto mb-4"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          {{ index + 1 }}
        </div>
        <h3 class="texto-glass font-semibold text-lg mb-2">{{ paso.titulo }}</h3>
        <p class="texto-glass-suave text-sm leading-relaxed">{{ paso.descripcion }}</p>
        <div
          v-if="index < pasos.length - 1"
          class="hidden md:block absolute -right-4 top-1/2 -translate-y-1/2 z-10"
        >
          <i class="pi pi-arrow-right texto-glass-suave text-xl" />
        </div>
      </div>
    </div>
  </div>
</section>

<!-- SECCIÓN 4: PRECIOS -->
<section id="precios" class="relative z-10 py-24 px-6">
  <div class="max-w-4xl mx-auto">
    <div class="text-center mb-16 scroll-oculto">
      <h2 class="text-3xl md:text-4xl font-bold texto-glass mb-4">
        Planes
        <span class="texto-gradiente">simples y transparentes</span>
      </h2>
      <p class="texto-glass-suave text-lg">Empieza gratis, escala cuando lo necesites.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
      <div class="glass p-8 scroll-oculto-izquierda delay-1">
        <h3 class="texto-glass font-bold text-xl mb-2">Gratuito</h3>
        <p class="texto-glass-suave text-sm mb-6">Para empezar a controlar tus finanzas</p>
        <div class="flex items-end gap-1 mb-6">
          <span class="text-4xl font-bold texto-glass">0€</span>
          <span class="texto-glass-suave text-sm mb-1">/mes</span>
        </div>
        <ul class="flex flex-col gap-3 mb-8">
          <li v-for="item in planGratuito" :key="item" class="flex items-center gap-2">
            <i class="pi pi-check text-green-400 text-sm" />
            <span class="texto-glass-suave text-sm">{{ item }}</span>
          </li>
        </ul>
        <RouterLink
          to="/registro"
          class="block text-center py-3 rounded-xl text-white font-medium transition-all hover:opacity-90"
          style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2)"
        >
          Empezar gratis
        </RouterLink>
      </div>

      <div class="glass p-8 relative overflow-hidden scroll-oculto-derecha delay-2">
        <div
          class="absolute top-4 right-4 px-3 py-1 rounded-full text-xs font-bold text-white"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          Próximamente
        </div>
        <h3 class="texto-glass font-bold text-xl mb-2">Pro</h3>
        <p class="texto-glass-suave text-sm mb-6">Para usuarios avanzados</p>
        <div class="flex items-end gap-1 mb-6">
          <span class="text-4xl font-bold texto-glass">4,99€</span>
          <span class="texto-glass-suave text-sm mb-1">/mes</span>
        </div>
        <ul class="flex flex-col gap-3 mb-8">
          <li v-for="item in planPro" :key="item" class="flex items-center gap-2">
            <i class="pi pi-check text-purple-400 text-sm" />
            <span class="texto-glass-suave text-sm">{{ item }}</span>
          </li>
        </ul>
        <button
          disabled
          class="w-full py-3 rounded-xl text-white font-medium opacity-50 cursor-not-allowed"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          Próximamente
        </button>
      </div>
    </div>
  </div>
</section>

<!-- SECCIÓN 5: CTA FINAL -->
<section class="relative z-10 py-24 px-6">
  <div class="max-w-2xl mx-auto text-center">
    <div class="glass p-12 rounded-3xl scroll-oculto-escala">
      <img src="/logo.png" alt="SGFP" class="w-16 h-16 rounded-2xl object-cover mx-auto mb-6" />
      <h2 class="text-3xl md:text-4xl font-bold texto-glass mb-4">
        Empieza hoy mismo
      </h2>
      <p class="texto-glass-suave text-lg mb-8">
        Únete y toma el control de tus finanzas personales de forma sencilla y visual.
      </p>
      <RouterLink
        to="/registro"
        class="inline-flex items-center gap-2 px-10 py-4 rounded-2xl text-white font-semibold text-lg transition-all hover:opacity-90 active:scale-95"
        style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
      >
        Crear cuenta gratis
        <i class="pi pi-arrow-right" />
      </RouterLink>
      <p class="texto-glass-suave text-sm mt-4">Sin tarjeta de crédito · Gratis para siempre</p>
    </div>
  </div>
</section>

    <!-- FOOTER -->
    <footer class="relative z-10 py-8 px-6" style="border-top: 1px solid rgba(255,255,255,0.08)">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <img src="/logo.png" alt="SGFP" class="w-7 h-7 rounded-lg object-cover" />
          <span class="texto-glass font-semibold">SGFP</span>
        </div>
        <p class="texto-glass-suave text-sm">© 2026 SGFP. Sistema de Gestión de Finanzas Personales.</p>
        <div class="flex items-center gap-4">
          <RouterLink to="/inicio-sesion" class="texto-glass-suave text-sm hover:text-white transition-colors">
            Iniciar sesión
          </RouterLink>
          <RouterLink to="/registro" class="texto-glass-suave text-sm hover:text-white transition-colors">
            Registrarse
          </RouterLink>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted } from 'vue'

onMounted(() => {
  // Intersection Observer para animaciones al hacer scroll
  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('scroll-visible')
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    }
  )

  // Observa todos los elementos con clases de animación
  document.querySelectorAll('.scroll-oculto, .scroll-oculto-izquierda, .scroll-oculto-derecha, .scroll-oculto-escala').forEach((el) => {
    observador.observe(el)
  })
})

function scrollTo(selector) {
  document.querySelector(selector)?.scrollIntoView({ behavior: 'smooth' })
}

const features = [
  {
    titulo: 'Dashboard intuitivo',
    descripcion: 'Visualiza tus ingresos, gastos y balance mensual con gráficos interactivos en tiempo real.',
    icono: 'pi pi-home',
    color: '#7c3aed'
  },
  {
    titulo: 'Control de transacciones',
    descripcion: 'Registra y categoriza cada movimiento financiero de forma rápida y organizada.',
    icono: 'pi pi-arrow-right-arrow-left',
    color: '#00b4d8'
  },
  {
    titulo: 'Presupuestos inteligentes',
    descripcion: 'Define límites mensuales por categoría y recibe alertas cuando te acerques al límite.',
    icono: 'pi pi-wallet',
    color: '#f59e0b'
  },
  {
    titulo: 'Recurrentes automáticos',
    descripcion: 'Automatiza tu sueldo, alquiler, suscripciones y cualquier gasto o ingreso periódico.',
    icono: 'pi pi-sync',
    color: '#10b981'
  },
  {
    titulo: 'Gestión de cuentas',
    descripcion: 'Controla el saldo de todas tus cuentas: efectivo, bancaria, tarjeta y ahorro.',
    icono: 'pi pi-credit-card',
    color: '#ec4899'
  },
  {
    titulo: 'PWA instalable',
    descripcion: 'Instala SGFP en tu móvil o escritorio y úsala como una app nativa sin conexión.',
    icono: 'pi pi-mobile',
    color: '#8b5cf6'
  }
]

const pasos = [
  {
    titulo: 'Crea tu cuenta',
    descripcion: 'Regístrate gratis en segundos. Sin tarjeta de crédito, sin complicaciones.'
  },
  {
    titulo: 'Configura tus cuentas',
    descripcion: 'Añade tus cuentas bancarias, efectivo y tarjetas con su saldo inicial.'
  },
  {
    titulo: 'Toma el control',
    descripcion: 'Registra transacciones, define presupuestos y visualiza tu situación financiera.'
  }
]

const planGratuito = [
  'Transacciones ilimitadas',
  'Hasta 5 categorías personalizadas',
  'Dashboard con gráficos',
  'Presupuestos mensuales',
  'Transacciones recurrentes',
  'PWA instalable'
]

const planPro = [
  'Todo lo del plan gratuito',
  'Categorías ilimitadas',
  'Exportar a PDF con gráficos',
  'Importar desde CSV',
  'Soporte prioritario',
  'Multi-divisa avanzado'
]

function scrollTo(selector) {
  document.querySelector(selector)?.scrollIntoView({ behavior: 'smooth' })
}
</script>