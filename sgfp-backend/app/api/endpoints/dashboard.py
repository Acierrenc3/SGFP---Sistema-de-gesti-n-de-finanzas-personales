# Endpoints del dashboard: datos agregados para el resumen financiero
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from datetime import datetime, date
import calendar
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.modelos.categoria import Categoria
from app.modelos.cuenta import Cuenta
from app.modelos.presupuesto import Presupuesto
from app.modelos.transaccion import Transaccion
from app.modelos.usuario import Usuario

enrutador = APIRouter()


class ResumenBalance(BaseModel):
    total_ingresos: float
    total_gastos: float
    balance: float


class GastoPorCategoria(BaseModel):
    id_categoria: int
    nombre_categoria: str
    total: float

    class Config:
        from_attributes = True


class EvolucionMensual(BaseModel):
    mes: int
    anio: int
    total_ingresos: float
    total_gastos: float


class ResumenPresupuesto(BaseModel):
    id_categoria: int
    nombre_categoria: str
    importe_limite: float
    gasto_actual: float
    porcentaje_usado: float

    class Config:
        from_attributes = True


class DisponibleDiario(BaseModel):
    presupuesto_total: float
    gasto_total: float
    presupuesto_restante: float
    dias_restantes: int
    disponible_diario: float


class PuntoEvolucionDiaria(BaseModel):
    fecha: str
    saldo: float
    ingresos: float
    gastos: float


class ResumenDashboard(BaseModel):
    balance: ResumenBalance
    gastos_por_categoria: List[GastoPorCategoria]
    evolucion_mensual: List[EvolucionMensual]
    resumen_presupuestos: List[ResumenPresupuesto]
    disponible_diario: Optional[DisponibleDiario] = None


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
    ahora = datetime.utcnow()
    mes_consulta = mes or ahora.month
    anio_consulta = anio or ahora.year

    # --- Balance ---
    total_ingresos = sesion.query(
        func.coalesce(func.sum(Transaccion.importe), 0.0)
    ).filter(
        Transaccion.id_usuario == usuario_actual.id,
        Transaccion.tipo == "ingreso",
        func.extract("month", Transaccion.fecha) == mes_consulta,
        func.extract("year", Transaccion.fecha) == anio_consulta
    ).scalar() or 0.0

    total_gastos = sesion.query(
        func.coalesce(func.sum(Transaccion.importe), 0.0)
    ).filter(
        Transaccion.id_usuario == usuario_actual.id,
        Transaccion.tipo == "gasto",
        func.extract("month", Transaccion.fecha) == mes_consulta,
        func.extract("year", Transaccion.fecha) == anio_consulta
    ).scalar() or 0.0

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

    # --- Evolución mensual ---
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
    presupuesto_total = 0.0
    gasto_total_presupuestado = 0.0

    for presupuesto in presupuestos:
        gasto_actual = sesion.query(
            func.coalesce(func.sum(Transaccion.importe), 0.0)
        ).filter(
            Transaccion.id_usuario == usuario_actual.id,
            Transaccion.id_categoria == presupuesto.id_categoria,
            Transaccion.tipo == "gasto",
            func.extract("month", Transaccion.fecha) == mes_consulta,
            func.extract("year", Transaccion.fecha) == anio_consulta
        ).scalar() or 0.0

        porcentaje = (
            (gasto_actual / presupuesto.importe_limite * 100)
            if presupuesto.importe_limite > 0
            else 0.0
        )

        categoria = sesion.query(Categoria).filter(
            Categoria.id == presupuesto.id_categoria
        ).first()

        resumen_presupuestos.append(
            ResumenPresupuesto(
                id_categoria=presupuesto.id_categoria,
                nombre_categoria=categoria.nombre if categoria else "Sin categoría",
                importe_limite=presupuesto.importe_limite,
                gasto_actual=gasto_actual,
                porcentaje_usado=round(porcentaje, 2)
            )
        )

        presupuesto_total += presupuesto.importe_limite
        gasto_total_presupuestado += gasto_actual

    # --- Disponible diario ---
    disponible_diario = None
    if presupuesto_total > 0:
        dias_en_mes = calendar.monthrange(anio_consulta, mes_consulta)[1]
        dia_actual = ahora.day if (
            mes_consulta == ahora.month and
            anio_consulta == ahora.year
        ) else dias_en_mes

        dias_restantes = max(dias_en_mes - dia_actual + 1, 1)
        presupuesto_restante = max(presupuesto_total - gasto_total_presupuestado, 0.0)
        diario = round(presupuesto_restante / dias_restantes, 2)

        disponible_diario = DisponibleDiario(
            presupuesto_total=round(presupuesto_total, 2),
            gasto_total=round(gasto_total_presupuestado, 2),
            presupuesto_restante=round(presupuesto_restante, 2),
            dias_restantes=dias_restantes,
            disponible_diario=diario
        )

    return ResumenDashboard(
        balance=balance,
        gastos_por_categoria=gastos_por_categoria,
        evolucion_mensual=evolucion_mensual,
        resumen_presupuestos=resumen_presupuestos,
        disponible_diario=disponible_diario
    )


@enrutador.get(
    "/evolucion-diaria",
    response_model=List[PuntoEvolucionDiaria],
    summary="Obtener evolución diaria del saldo"
)
def obtener_evolucion_diaria(
    mes: Optional[int] = Query(None, description="Mes a consultar (1-12)"),
    anio: Optional[int] = Query(None, description="Año a consultar"),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve la evolución diaria del saldo durante el mes indicado.
    Parte del saldo inicial de las cuentas y acumula ingresos/gastos día a día.
    """
    ahora = datetime.utcnow()
    mes_consulta = mes or ahora.month
    anio_consulta = anio or ahora.year

    # Saldo inicial de todas las cuentas del usuario
    saldo_inicial = sesion.query(
        func.coalesce(func.sum(Cuenta.saldo_inicial), 0.0)
    ).filter(
        Cuenta.id_usuario == usuario_actual.id
    ).scalar() or 0.0

    # Transacciones anteriores al mes consultado
    saldo_anterior = sesion.query(
        func.coalesce(func.sum(
            func.case(
                (Transaccion.tipo == 'ingreso', Transaccion.importe),
                else_=-Transaccion.importe
            )
        ), 0.0)
    ).filter(
        Transaccion.id_usuario == usuario_actual.id,
        Transaccion.fecha < datetime(anio_consulta, mes_consulta, 1)
    ).scalar() or 0.0

    saldo_base = saldo_inicial + saldo_anterior

    # Transacciones del mes agrupadas por día
    transacciones_mes = sesion.query(
        func.date(Transaccion.fecha).label('dia'),
        Transaccion.tipo,
        func.sum(Transaccion.importe).label('total')
    ).filter(
        Transaccion.id_usuario == usuario_actual.id,
        func.extract('month', Transaccion.fecha) == mes_consulta,
        func.extract('year', Transaccion.fecha) == anio_consulta
    ).group_by(
        func.date(Transaccion.fecha),
        Transaccion.tipo
    ).order_by(
        func.date(Transaccion.fecha)
    ).all()

    # Construye diccionario por día
    dias_dict = {}
    for fila in transacciones_mes:
        dia_str = str(fila.dia)
        if dia_str not in dias_dict:
            dias_dict[dia_str] = {'ingresos': 0.0, 'gastos': 0.0}
        if fila.tipo == 'ingreso':
            dias_dict[dia_str]['ingresos'] = float(fila.total)
        else:
            dias_dict[dia_str]['gastos'] = float(fila.total)

    # Genera serie diaria
    dias_en_mes = calendar.monthrange(anio_consulta, mes_consulta)[1]
    dia_actual = ahora.day if (
        mes_consulta == ahora.month and
        anio_consulta == ahora.year
    ) else dias_en_mes

    saldo_acumulado = saldo_base
    serie = []

    for dia in range(1, dia_actual + 1):
        fecha_str = date(anio_consulta, mes_consulta, dia).isoformat()
        movimientos = dias_dict.get(fecha_str, {'ingresos': 0.0, 'gastos': 0.0})
        saldo_acumulado += movimientos['ingresos'] - movimientos['gastos']
        serie.append(PuntoEvolucionDiaria(
            fecha=fecha_str,
            saldo=round(saldo_acumulado, 2),
            ingresos=movimientos['ingresos'],
            gastos=movimientos['gastos']
        ))

    return serie