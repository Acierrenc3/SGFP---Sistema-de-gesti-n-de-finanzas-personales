# Endpoints de exportación de datos
# Basado en: https://fastapi.tiangolo.com/advanced/custom-response/

import csv
import io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.modelos.categoria import Categoria
from app.modelos.cuenta import Cuenta
from app.modelos.transaccion import Transaccion
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints de exportación
enrutador = APIRouter()


@enrutador.get(
    "/csv",
    summary="Exportar transacciones a CSV",
    response_class=StreamingResponse
)
def exportar_csv(
    mes: Optional[int] = Query(None, description="Filtrar por mes (1-12)"),
    anio: Optional[int] = Query(None, description="Filtrar por año"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: 'ingreso' o 'gasto'"),
    id_categoria: Optional[int] = Query(None, description="Filtrar por categoría"),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Exporta las transacciones del usuario autenticado en formato CSV.
    Permite filtrar por mes, año, tipo y categoría.
    Devuelve el archivo como descarga directa en el navegador.
    """
    # Construye la consulta base
    consulta = sesion.query(Transaccion).filter(
        Transaccion.id_usuario == usuario_actual.id
    )

    # Aplica filtros opcionales
    if mes:
        from sqlalchemy import func
        consulta = consulta.filter(
            func.extract("month", Transaccion.fecha) == mes
        )
    if anio:
        from sqlalchemy import func
        consulta = consulta.filter(
            func.extract("year", Transaccion.fecha) == anio
        )
    if tipo:
        consulta = consulta.filter(Transaccion.tipo == tipo)
    if id_categoria:
        consulta = consulta.filter(Transaccion.id_categoria == id_categoria)

    transacciones = consulta.order_by(Transaccion.fecha.desc()).all()

    # Genera el archivo CSV en memoria usando StringIO
    # Basado en: https://docs.python.org/3/library/csv.html
    salida = io.StringIO()
    escritor = csv.writer(salida, delimiter=";", quoting=csv.QUOTE_MINIMAL)

    # Cabecera del CSV
    escritor.writerow([
        "ID",
        "Tipo",
        "Importe",
        "Fecha",
        "Descripción",
        "Categoría",
        "Cuenta"
    ])

    # Filas de datos
    for transaccion in transacciones:
        # Obtiene el nombre de la categoría
        categoria = sesion.query(Categoria).filter(
            Categoria.id == transaccion.id_categoria
        ).first()

        # Obtiene el nombre de la cuenta
        cuenta = sesion.query(Cuenta).filter(
            Cuenta.id == transaccion.id_cuenta
        ).first()

        escritor.writerow([
            transaccion.id,
            transaccion.tipo,
            f"{transaccion.importe:.2f}",
            transaccion.fecha.strftime("%d/%m/%Y %H:%M"),
            transaccion.descripcion or "",
            categoria.nombre if categoria else "",
            cuenta.nombre if cuenta else ""
        ])

    # Mueve el cursor al inicio del buffer
    salida.seek(0)

    # Genera el nombre del archivo con la fecha actual
    nombre_archivo = f"sgfp_transacciones_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"

    # Devuelve el CSV como respuesta de descarga
    return StreamingResponse(
        iter([salida.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={nombre_archivo}"
        }
    )