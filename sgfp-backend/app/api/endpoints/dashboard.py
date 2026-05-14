# Endpoints del dashboard: datos agregados para el resumen financiero
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.modelos.categoria import Categoria
from app.modelos.presupuesto import Presupuesto
from app.modelos.transaccion import Transaccion
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints del dashboard
enrutador = APIRouter()


# Esquemas de respuesta específicos del dashboard
class ResumenBalance(BaseModel):
    """Resumen del balance total del usuario en el período indicado."""
    total_ingresos: float
    total_gastos: float
    balance: float


class GastoPorCategoria(BaseModel):
    """Gasto agrupado por categoría para el período indicado."""
    id_categoria: int
    nombre_categoria: str
    total: float

    class Config:
        from_attributes = True


class EvolucionMensual(BaseModel):
    """Ingresos y gastos agrupados por mes."""
    mes: int
    anio: int
    total_ingresos: float
    total_gastos: float


class ResumenPresupuesto(BaseModel):
    """Estado del presupuesto por categoría: límite vs gasto real."""
    id_categoria: int
    nombre_categoria: str
    importe_limite: float
    gasto_actual: float
    porcentaje_usado: float

    class Config:
        from_attributes = True


class ResumenDashboard(BaseModel):
    """Respuesta completa del dashboard con todos los datos agregados."""
    balance: ResumenBalance
    gastos_por_categoria: List[GastoPorCategoria]
    evolucion_mensual: List[EvolucionMensual]
    resumen_presupuestos: List[ResumenPresupuesto]


@enrutador.get(
    "/resumen",
    response_model=ResumenDashboard,
    summary="Obtener datos agregados para el dashboard"
)
def obtener_resumen_dashboard(
    mes: Optional[int] = Query(None, description="Mes a consultar (1-12)"),
    anio: Optional[int] = Query(None, description="Año a consultar"),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve un resumen completo de las finanzas del usuario:
    - Balance total (ingresos, gastos y diferencia)
    - Gastos agrupados por categoría
    - Evolución mensual de ingresos y gastos
    - Estado de los presupuestos por categoría
    Si no se indica mes/año, usa el mes y año actuales.
    """
    # Usa el mes y año actuales si no se indican
    ahora = datetime.utcnow()
    mes_consulta = mes or ahora.month
    anio_consulta = anio or ahora.year

    # Filtra transacciones del usuario en el período indicado
    consulta_base = sesion.query(Transaccion).filter(
        Transaccion.id_usuario == usuario_actual.id,
        func.extract("month", Transaccion.fecha) == mes_consulta,
        func.extract("year", Transaccion.fecha) == anio_consulta
    )

    # --- Balance ---
    total_ingresos = sesion.query(
        func.coalesce(func.sum(Transaccion.importe), 0.0)
    ).filter(
        Transaccion.id_usuario == usuario_actual.id,
        Transaccion.tipo == "ingreso",
        func.extract("month", Transaccion.fecha) == mes_consulta,
        func.extract("year", Transaccion.fecha) == anio_consulta
    ).scalar()

    total_gastos = sesion.query(
        func.coalesce(func.sum(Transaccion.importe), 0.0)
    ).filter(
        Transaccion.id_usuario == usuario_actual.id,
        Transaccion.tipo == "gasto",
        func.extract("month", Transaccion.fecha) == mes_consulta,
        func.extract("year", Transaccion.fecha) == anio_consulta
    ).scalar()

    balance = ResumenBalance(
        total_ingresos=total_ingresos,
        total_gastos=total_gastos,
        balance=total_ingresos - total_gastos
    )

    # --- Gastos por categoría ---
    gastos_por_categoria_query = sesion.query(
        Transaccion.id_categoria,
        Categoria.nombre,
        func.sum(Transaccion.importe).label("total")
    ).join(
        Categoria, Transaccion.id_categoria == Categoria.id
    ).filter(
        Transaccion.id_usuario == usuario_actual.id,
        Transaccion.tipo == "gasto",
        func.extract("month", Transaccion.fecha) == mes_consulta,
        func.extract("year", Transaccion.fecha) == anio_consulta
    ).group_by(
        Transaccion.id_categoria,
        Categoria.nombre
    ).all()

    gastos_por_categoria = [
        GastoPorCategoria(
            id_categoria=fila.id_categoria,
            nombre_categoria=fila.nombre,
            total=fila.total
        )
        for fila in gastos_por_categoria_query
    ]

    # --- Evolución mensual (últimos 6 meses) ---
    evolucion_query = sesion.query(
        func.extract("month", Transaccion.fecha).label("mes"),
        func.extract("year", Transaccion.fecha).label("anio"),
        Transaccion.tipo,
        func.sum(Transaccion.importe).label("total")
    ).filter(
        Transaccion.id_usuario == usuario_actual.id
    ).group_by(
        func.extract("month", Transaccion.fecha),
        func.extract("year", Transaccion.fecha),
        Transaccion.tipo
    ).order_by(
        func.extract("year", Transaccion.fecha).desc(),
        func.extract("month", Transaccion.fecha).desc()
    ).limit(12).all()

    # Agrupa ingresos y gastos por mes/año
    evolucion_dict: dict = {}
    for fila in evolucion_query:
        clave = (int(fila.mes), int(fila.anio))
        if clave not in evolucion_dict:
            evolucion_dict[clave] = {"total_ingresos": 0.0, "total_gastos": 0.0}
        if fila.tipo == "ingreso":
            evolucion_dict[clave]["total_ingresos"] = fila.total
        else:
            evolucion_dict[clave]["total_gastos"] = fila.total

    evolucion_mensual = [
        EvolucionMensual(
            mes=clave[0],
            anio=clave[1],
            total_ingresos=valores["total_ingresos"],
            total_gastos=valores["total_gastos"]
        )
        for clave, valores in evolucion_dict.items()
    ]

    # --- Resumen de presupuestos ---
    presupuestos = sesion.query(Presupuesto).filter(
        Presupuesto.id_usuario == usuario_actual.id,
        Presupuesto.mes == mes_consulta,
        Presupuesto.anio == anio_consulta
    ).all()

    resumen_presupuestos = []
    for presupuesto in presupuestos:
        # Calcula el gasto real de la categoría en el período
        gasto_actual = sesion.query(
            func.coalesce(func.sum(Transaccion.importe), 0.0)
        ).filter(
            Transaccion.id_usuario == usuario_actual.id,
            Transaccion.id_categoria == presupuesto.id_categoria,
            Transaccion.tipo == "gasto",
            func.extract("month", Transaccion.fecha) == mes_consulta,
            func.extract("year", Transaccion.fecha) == anio_consulta
        ).scalar()

        # Calcula el porcentaje usado del presupuesto
        porcentaje = (
            (gasto_actual / presupuesto.importe_limite * 100)
            if presupuesto.importe_limite > 0
            else 0.0
        )

        categoria = sesion.qu