// Store de notificaciones con Pinia
// Basado en: https://pinia.vuejs.org/core-concepts/

import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../servicios/api'

export const useNotificacionesStore = defineStore('notificaciones', () => {
    const notificaciones = ref([])
    const cargando = ref(false)

    async function verificarPresupuestos() {
        try {
            const ahora = new Date()
            const respuesta = await api.get('/dashboard/resumen', {
                params: {
                    mes: ahora.getMonth() + 1,
                    anio: ahora.getFullYear()
                }
            })

            const nuevasNotificaciones = []

            respuesta.data.resumen_presupuestos.forEach(presupuesto => {
                const porcentaje = presupuesto.porcentaje_usado

                if (porcentaje >= 100) {
                    nuevasNotificaciones.push({
                        id: `presupuesto-${presupuesto.id_categoria}-100`,
                        tipo: 'error',
                        categoria: presupuesto.nombre_categoria,
                        porcentaje,
                        mensaje: `¡Límite superado! Has gastado el 100% del presupuesto de ${presupuesto.nombre_categoria}`,
                        icono: 'pi pi-times-circle'
                    })
                } else if (porcentaje >= 80) {
                    nuevasNotificaciones.push({
                        id: `presupuesto-${presupuesto.id_categoria}-80`,
                        tipo: 'warning',
                        categoria: presupuesto.nombre_categoria,
                        porcentaje,
                        mensaje: `Atención: Has usado el ${porcentaje.toFixed(0)}% del presupuesto de ${presupuesto.nombre_categoria}`,
                        icono: 'pi pi-exclamation-triangle'
                    })
                } else if (porcentaje >= 50) {
                    nuevasNotificaciones.push({
                        id: `presupuesto-${presupuesto.id_categoria}-50`,
                        tipo: 'info',
                        categoria: presupuesto.nombre_categoria,
                        porcentaje,
                        mensaje: `Has usado el ${porcentaje.toFixed(0)}% del presupuesto de ${presupuesto.nombre_categoria}`,
                        icono: 'pi pi-info-circle'
                    })
                }
            })

            notificaciones.value = nuevasNotificaciones
        } catch {
            // Si falla no bloqueamos la app
        }
    }

    function limpiarNotificaciones() {
        notificaciones.value = []
    }

    return {
        notificaciones,
        cargando,
        verificarPresupuestos,
        limpiarNotificaciones
    }
})