# Endpoints de transacciones: CRUD completo
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List, Optional
from datetime import datetime
import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.core.websocket_manager import gestor_ws
from app.db.sesion import obtener_sesion
from app.esquemas.transaccion import (
    TransaccionActualizar,
    TransaccionCrear,
    TransaccionRespuesta
)
from app.modelos.desglose import DesgloseTransaccion
from app.modelos.presupuesto import Presupuesto
from app.modelos.categoria import Categoria
from app.modelos.transaccion import Transaccion
from app.modelos.usuario import Usuario

enrutador = APIRouter()


def sincronizar_desgloses(sesion: Session, transaccion: Transaccion, desgloses: list):
    """Elimina los desgloses existentes y crea los nuevos."""
    for desglose in transaccion.desgloses:
        sesion.delete(desglose)
    sesion.flush()

    for datos in desgloses:
        nuevo = DesgloseTransaccion(
            concepto=datos.concepto,
            importe=datos.importe,
            id_transaccion=transaccion.id
        )
        sesion.add(nuevo)


async def verificar_y_notificar_presupuesto(
    sesion: Session,
    id_usuario: int,
    id_categoria: int,
    fecha: datetime
):
    """
    Verifica el estado del presupuesto tras una transacción
    y envía notificación WebSocket si supera umbrales.
    """
    try:
        presupuesto = sesion.query(Presupuesto).filter(
            Presupuesto.id_usuario == id_usuario,
            Presupuesto.id_categoria == id_categoria,
            Presupuesto.mes == fecha.month,
            Presupuesto.anio == fecha.year
        ).first()

        if not presupuesto:
            return

        # Calcula el gasto actual
        gasto_actual = sesion.query(
            func.coalesce(func.sum(Transaccion.importe), 0)
        ).filter(
            Transaccion.id_usuario == id_usuario,
            Transaccion.id_categoria == id_categoria,
            Transaccion.tipo == 'gasto',
            func.extract('month', Transaccion.fecha) == fecha.month,
            func.extract('year', Transaccion.fecha) == fecha.year
        ).scalar()

        porcentaje = (float(gasto_actual) / presupuesto.importe_limite) * 100

        # Obtiene el nombre de la categoría
        categoria = sesion.query(Categoria).filter(
            Categoria.id == id_categoria
        ).first()
        nombre_categoria = categoria.nombre if categoria else "Categoría"

        # Envía notificación según umbral
        if porcentaje >= 100:
            await gestor_ws.enviar_a_usuario(id_usuario, {
                "tipo": "presupuesto_superado",
                "categoria": nombre_categoria,
                "porcentaje": round(porcentaje, 1),
                "mensaje": f"Has superado el presupuesto de {nombre_categoria} ({round(porcentaje, 1)}%)",
                "icono": "pi-exclamation-circle",
                "nivel": "error"
            })
        elif porcentaje >= 80:
            await gestor_ws.enviar_a_usuario(id_usuario, {
                "tipo": "presupuesto_alerta",
                "categoria": nombre_categoria,
                "porcentaje": round(porcentaje, 1),
                "mensaje": f"Llevas el {round(porcentaje, 1)}% del presupuesto de {nombre_categoria}",
                "icono": "pi-exclamation-triangle",
                "nivel": "warning"
            })
        elif porcentaje >= 50:
            await gestor_ws.enviar_a_usuario(id_usuario, {
                "tipo": "presupuesto_info",
                "categoria": nombre_categoria,
                "porcentaje": round(porcentaje, 1),
                "mensaje": f"Llevas el {round(porcentaje, 1)}% del presupuesto de {nombre_categoria}",
                "icono": "pi-info-circle",
                "nivel": "info"
            })
    except Exception:
        pass


@enrutador.get(
    "/",
    summary="Listar transacciones del usuario con paginación"
)
def listar_transacciones(
    tipo: Optional[str] = Query(None),
    id_categoria: Optional[int] = Query(None),
    id_cuenta: Optional[int] = Query(None),
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    descripcion: Optional[str] = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    consulta = sesion.query(Transaccion).filter(
        Transaccion.id_usuario == usuario_actual.id
    )

    if tipo:
        consulta = consulta.filter(Transaccion.tipo == tipo)
    if id_categoria:
        consulta = consulta.filter(Transaccion.id_categoria == id_categoria)
    if id_cuenta:
        consulta = consulta.filter(Transaccion.id_cuenta == id_cuenta)
    if fecha_inicio:
        fecha_inicio = fecha_inicio.replace(tzinfo=None)
        consulta = consulta.filter(Transaccion.fecha >= fecha_inicio)
    if fecha_fin:
        fecha_fin = fecha_fin.replace(tzinfo=None)
        consulta = consulta.filter(Transaccion.fecha <= fecha_fin)
    if descripcion:
        consulta = consulta.filter(
            Transaccion.descripcion.ilike(f"%{descripcion}%")
        )

    total = consulta.count()
    transacciones = consulta.order_by(
        Transaccion.fecha.desc()
    ).offset((pagina - 1) * limite).limit(limite).all()

    return {
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "paginas": (total + limite - 1) // limite,
        "transacciones": [TransaccionRespuesta.model_validate(t) for t in transacciones]
    }


@enrutador.post(
    "/",
    response_model=TransaccionRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva transacción"
)
async def crear_transaccion(
    datos: TransaccionCrear,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    desgloses = datos.desgloses or []
    datos_transaccion = datos.model_dump(exclude={"desgloses"})

    nueva_transaccion = Transaccion(
        **datos_transaccion,
        id_usuario=usuario_actual.id
    )

    sesion.add(nueva_transaccion)
    sesion.commit()
    sesion.refresh(nueva_transaccion)

    for desglose in desgloses:
        nuevo = DesgloseTransaccion(
            concepto=desglose.concepto,
            importe=desglose.importe,
            id_transaccion=nueva_transaccion.id
        )
        sesion.add(nuevo)

    sesion.commit()
    sesion.refresh(nueva_transaccion)

    # Notifica si es un gasto y hay presupuesto
    if nueva_transaccion.tipo == 'gasto':
        await verificar_y_notificar_presupuesto(
            sesion,
            usuario_actual.id,
            nueva_transaccion.id_categoria,
            nueva_transaccion.fecha
        )

    return nueva_transaccion


@enrutador.get(
    "/{id}",
    response_model=TransaccionRespuesta,
    summary="Obtener transacción por ID"
)
def obtener_transaccion(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    transaccion = sesion.query(Transaccion).filter(
        Transaccion.id == id,
        Transaccion.id_usuario == usuario_actual.id
    ).first()

    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )

    return transaccion


@enrutador.put(
    "/{id}",
    response_model=TransaccionRespuesta,
    summary="Actualizar transacción existente"
)
async def actualizar_transaccion(
    id: int,
    datos: TransaccionActualizar,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    transaccion = sesion.query(Transaccion).filter(
        Transaccion.id == id,
        Transaccion.id_usuario == usuario_actual.id
    ).first()

    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )

    desgloses = datos.desgloses
    datos_actualizados = datos.model_dump(exclude_unset=True, exclude={"desgloses"})

    for campo, valor in datos_actualizados.items():
        setattr(transaccion, campo, valor)

    if desgloses is not None:
        sincronizar_desgloses(sesion, transaccion, desgloses)

    sesion.commit()
    sesion.refresh(transaccion)

    # Notifica si es un gasto y hay presupuesto
    if transaccion.tipo == 'gasto':
        await verificar_y_notificar_presupuesto(
            sesion,
            usuario_actual.id,
            transaccion.id_categoria,
            transaccion.fecha
        )

    return transaccion


@enrutador.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar transacción"
)
def eliminar_transaccion(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    transaccion = sesion.query(Transaccion).filter(
        Transaccion.id == id,
        Transaccion.id_usuario == usuario_actual.id
    ).first()

    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )

    sesion.delete(transaccion)
    sesion.commit()