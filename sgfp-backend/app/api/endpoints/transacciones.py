# Endpoints de transacciones: CRUD completo
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.esquemas.transaccion import (
    TransaccionActualizar,
    TransaccionCrear,
    TransaccionRespuesta
)
from app.modelos.desglose import DesgloseTransaccion
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
def crear_transaccion(
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
def actualizar_transaccion(
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