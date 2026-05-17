<template>
  <LayoutPrincipal>
    <div class="p-6">
      <!-- Cabecera -->
      <div class="flex items-center justify-between mb-8 animar-lateral">
        <div>
          <h2 class="text-2xl font-bold texto-glass">Presupuestos</h2>
          <p class="texto-glass-suave text-sm mt-1">Gestiona tus límites de gasto mensuales</p>
        </div>
        <button
          @click="abrirDialogo()"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-white text-sm font-medium transition-all hover:opacity-90 active:scale-95"
          style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
        >
          <i class="pi pi-plus" />
          Nuevo presupuesto
        </button>
      </div>

      <!-- Filtros -->
      <div class="glass p-4 mb-4 animar-entrada">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <select
            v-model="filtros.mes"
            @change="cargarPresupuestos"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option value="" class="bg-gray-900">Todos los meses</option>
            <option v-for="mes in meses" :key="mes.valor" :value="mes.valor" class="bg-gray-900">
              {{ mes.etiqueta }}
            </option>
          </select>
          <select
            v-model="filtros.anio"
            @change="cargarPresupuestos"
            class="px-4 py-2 rounded-xl text-white text-sm outline-none cursor-pointer"
            style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
          >
            <option value="" class="bg-gray-900">Todos los años</option>
            <option v-for="anio in anios" :key="anio" :value="anio" class="bg-gray-900">
              {{ anio }}
            </option>
          </select>
        </div>
      </div>

      <!-- Grid de presupuestos -->
      <div v-if="cargando" class="flex justify-center py-12">
        <i class="pi pi-spin pi-spinner text-2xl texto-glass-suave" />
      </div>

      <div v-else-if="presupuestos.length === 0" class="glass flex flex-col items-center py-12 texto-glass-suave animar-entrada">
        <i class="pi pi-wallet text-4xl mb-2 opacity-30" />
        <p class="text-sm">No hay presupuestos registrados</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="presupuesto in presupuestos"
          :key="presupuesto.id"
          class="glass p-5 group animar-entrada"
        >
          <!-- Cabecera tarjeta -->
          <div class="flex items-center justify-between mb-4">
            <div>
              <p class="texto-glass font-medium text-sm">{{ obtenerNombreCategoria(presupuesto.id_categoria) }}</p>
              <p class="texto-glass-suave text-xs mt-0.5">
                {{ obtenerNombreMes(presupuesto.mes) }} {{ presupuesto.anio }}
              </p>
            </div>
            <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                @click="abrirDialogo(presupuesto)"
                class="w-7 h-7 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-pencil text-xs" />
              </button>
              <button
                @click="confirmarEliminar(presupuesto)"
                class="w-7 h-7 rounded-lg flex items-center justify-center text-red-400/50 hover:text-red-400 transition-colors"
                style="background: rgba(255,255,255,0.08)"
              >
                <i class="pi pi-trash text-xs" />
              </button>
            </div>
          </div>

          <!-- Importe límite -->
          <p class="text-2xl font-bold texto-glass mb-3">
            {{ formatearMoneda(presupuesto.importe_limite) }}
          </p>

          <!-- Barra de progreso real -->
          <div class="w-full h-1.5 rounded-full mt-3" style="background: rgba(255,255,255,0.1)">
            <div
              class="h-1.5 rounded-full animar-progreso"
              :style="{
                width: `${Math.min(gastosReales[presupuesto.id_categoria]?.porcentaje_usado || 0, 100)}%`,
                background: (gastosReales[presupuesto.id_categoria]?.porcentaje_usado || 0) >= 100
                  ? 'linear-gradient(90deg, #ef4444, #dc2626)'
                  : (gastosReales[presupuesto.id_categoria]?.porcentaje_usado || 0) >= 80
                  ? 'linear-gradient(90deg, #f59e0b, #d97706)'
                  : 'linear-gradient(90deg, #7c3aed, #00b4d8)'
              }"
            />
          </div>
          <div class="flex justify-between mt-1">
            <p class="texto-glass-suave text-xs">
              {{ formatearMoneda(gastosReales[presupuesto.id_categoria]?.gasto_actual || 0) }} gastado
            </p>
            <p
              class="text-xs font-medium"
              :style="(gastosReales[presupuesto.id_categoria]?.porcentaje_usado || 0) >= 100
                ? 'color: #f87171'
                : (gastosReales[presupuesto.id_categoria]?.porcentaje_usado || 0) >= 80
                ? 'color: #fbbf24'
                : 'color: rgba(255,255,255,0.5)'"
            >
              {{ (gastosReales[presupuesto.id_categoria]?.porcentaje_usado || 0).toFixed(1) }}%
            </p>
          </div>
        </div>
      </div>

      <!-- Diálogo crear/editar -->
      <div
        v-if="dialogoVisible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px)"
        @click.self="dialogoVisible = false"
      >
        <div class="glass w-full max-w-md p-6 animar-dialogo">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-bold texto-glass">
              {{ presupuestoEditando ? 'Editar presupuesto' : 'Nuevo presupuesto' }}
            </h3>
            <button
              @click="dialogoVisible = false"
              class="w-8 h-8 rounded-lg flex items-center justify-center texto-glass-suave hover:text-white transition-colors"
              style="background: rgba(255,255,255,0.08)"
            >
              <i class="pi pi-times text-sm" />
            </button>
          </div>

          <form @submit.prevent="guardarPresupuesto" class="flex flex-col gap-4">
            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Categoría</label>
              <select
                v-model="formulario.id_categoria"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.id_categoria ? 'border-red-400' : 'focus:border-purple-400'"
              >
                <option value="" class="bg-gray-900">Selecciona una categoría</option>
                <option v-for="cat in categorias" :key="cat.id" :value="cat.id" class="bg-gray-900">
                  {{ cat.nombre }}
                </option>
              </select>
              <small class="text-red-400" v-if="errores.id_categoria">{{ errores.id_categoria }}</small>
            </div>

            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Mes</label>
              <select
                v-model="formulario.mes"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.mes ? 'border-red-400' : 'focus:border-purple-400'"
              >
                <option value="" class="bg-gray-900">Selecciona un mes</option>
                <option v-for="mes in meses" :key="mes.valor" :value="mes.valor" class="bg-gray-900">
                  {{ mes.etiqueta }}
                </option>
              </select>
              <small class="text-red-400" v-if="errores.mes">{{ errores.mes }}</small>
            </div>

            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Año</label>
              <select
                v-model="formulario.anio"
                class="w-full px-4 py-3 rounded-xl text-white outline-none cursor-pointer"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.anio ? 'border-red-400' : 'focus:border-purple-400'"
              >
                <option value="" class="bg-gray-900">Selecciona un año</option>
                <option v-for="anio in anios" :key="anio" :value="anio" class="bg-gray-900">
                  {{ anio }}
                </option>
              </select>
              <small class="text-red-400" v-if="errores.anio">{{ errores.anio }}</small>
            </div>

            <div class="flex flex-col gap-2">
              <label class="texto-glass text-sm font-medium">Importe límite</label>
              <input
                v-model="formulario.importe_limite"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                class="w-full px-4 py-3 rounded-xl text-white placeholder-white/40 outline-none transition-all"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15)"
                :class="errores.importe_limite ? 'border-red-400' : 'focus:border-purple-400'"
              />
              <small class="text-red-400" v-if="errores.importe_limite">{{ errores.importe_limite }}</small>
            </div>

            <div class="flex gap-3 mt-2">
              <button
                type="button"
                @click="dialogoVisible = false"
                class="flex-1 py-3 rounded-xl text-sm font-medium texto-glass-suave transition-all hover:text-white"
                style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1)"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="guardando"
                class="flex-1 py-3 rounded-xl text-sm font-semibold text-white transition-all hover:opacity-90 disabled:opacity-50"
                style="background: linear-gradient(135deg, #7c3aed, #00b4d8)"
              >
                <span v-if="!guardando">{{ presupuestoEditando ? 'Guardar cambios' : 'Crear presupuesto' }}</span>
                <i v-else class="pi pi-spin pi-spinner" />
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Diálogo confirmar eliminar -->
      <div
        v-if="dialogoEliminarVisible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="background: rgba(0,0,0,0.5); backdrop-filter: blur(4px)"
      >
        <div class="glass w-full max-w-sm p-6 text-center animar-dialogo">
          <div class="w-14 h-14 rounded-full flex items-center justify-center mx-auto mb-4"
            style="background: rgba(239,68,68,0.15)">
            <i class="pi pi-exclamation-triangle text-red-400 text-2xl" />
          </div>
          <h3 class="text-lg font-bold texto-glass mb-2">¿Eliminar presupuesto?</h3>
          <p class="texto-glass-suave text-sm mb-6">Esta acción no se puede deshacer.</p>
          <div class="flex gap-3">
            <button
              @click="dialogoEliminarVisible = false"
              class="flex-1 py-2 rounded-xl text-sm font-medium texto-glass-suave transition-all hover:text-white"
              style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1)"
            >
              Cancelar
            </button>
            <button
              @click="eliminarPresupuesto"
              class="flex-1 py-2 rounded-xl text-sm font-semibold text-white transition-all hover:opacity-90"
              style="background: linear-gradient(135deg, #ef4444, #dc2626)"
            >
              Sí, eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
  </LayoutPrincipal>
</template>