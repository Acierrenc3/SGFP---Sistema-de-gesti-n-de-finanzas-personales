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
from app.modelos.transaccion import Transaccion
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints de transacciones
enrutador = APIRouter()


@enrutador.get(
    "/",
    response_model=List[TransaccionRespuesta],
    summary="Listar transacciones del usuario"
)
def listar_transacciones(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: 'ingreso' o 'gasto'"),
    id_categoria: Optional[int] = Query(None, description="Filtrar por categoría"),
    id_cuenta: Optional[int] = Query(None, description="Filtrar por cuenta"),
    fecha_inicio: Optional[datetime] = Query(None, description="Filtrar desde esta fecha"),
    fecha_fin: Optional[datetime] = Query(None, description="Filtrar hasta esta fecha"),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve todas las transacciones del usuario autenticado.
    Permite filtrar por tipo, categoría, cuenta y rango de fechas.
    """
    consulta = sesion.query(Transaccion).filter(
        Transaccion.id_usuario == usuario_actual.id
    )

    # Aplica filtros opcionales
    if tipo:
        consulta = consulta.filter(Transaccion.tipo == tipo)
    if id_categoria:
        consulta = consulta.filter(Transaccion.id_categoria == id_categoria)
    if id_cuenta:
        consulta = consulta.filter(Transaccion.id_cuenta == id_cuenta)
    if fecha_inicio:
        consulta = consulta.filter(Transaccion.fecha >= fecha_inicio)
    if fecha_fin:
        consulta = consulta.filter(Transaccion.fecha <= fecha_fin)

    return consulta.order_by(Transaccion.fecha.desc()).all()


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
    """
    Crea una nueva transacción vinculada al usuario autenticado.
    """
    nueva_transaccion = Transaccion(
        **datos.model_dump(),
        id_usuario=usuario_actual.id
    )

    sesion.add(nueva_transaccion)
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
    """
    Devuelve una transacción específica del usuario autenticado.
    """
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
    """
    Actualiza los campos indicados de una transacción existente.
    Solo permite modificar transacciones del usuario autenticado.
    """
    transaccion = sesion.query(Transaccion).filter(
        Transaccion.id == id,
        Transaccion.id_usuario == usuario_actual.id
    ).first()

    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )

    # Actualiza solo los campos enviados en la petición
    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(transaccion, campo, valor)

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
    """
    Elimina una transacción del usuario autenticado.
    """
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