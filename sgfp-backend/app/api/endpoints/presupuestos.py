# Endpoints de presupuestos: CRUD completo
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.esquemas.presupuesto import (
    PresupuestoActualizar,
    PresupuestoCrear,
    PresupuestoRespuesta
)
from app.modelos.presupuesto import Presupuesto
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints de presupuestos
enrutador = APIRouter()


@enrutador.get(
    "/",
    response_model=List[PresupuestoRespuesta],
    summary="Listar presupuestos del usuario"
)
def listar_presupuestos(
    mes: Optional[int] = Query(None, description="Filtrar por mes (1-12)"),
    anio: Optional[int] = Query(None, description="Filtrar por año"),
    id_categoria: Optional[int] = Query(None, description="Filtrar por categoría"),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve todos los presupuestos del usuario autenticado.
    Permite filtrar por mes, año y categoría.
    """
    consulta = sesion.query(Presupuesto).filter(
        Presupuesto.id_usuario == usuario_actual.id
    )

    # Aplica filtros opcionales
    if mes:
        consulta = consulta.filter(Presupuesto.mes == mes)
    if anio:
        consulta = consulta.filter(Presupuesto.anio == anio)
    if id_categoria:
        consulta = consulta.filter(Presupuesto.id_categoria == id_categoria)

    return consulta.order_by(Presupuesto.anio.desc(), Presupuesto.mes.desc()).all()


@enrutador.post(
    "/",
    response_model=PresupuestoRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo presupuesto mensual"
)
def crear_presupuesto(
    datos: PresupuestoCrear,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Crea un nuevo presupuesto mensual por categoría.
    Verifica que no exista ya un presupuesto para la misma
    categoría, mes y año del usuario autenticado.
    """
    # Comprueba si ya existe un presupuesto para esa categoría y mes
    presupuesto_existente = sesion.query(Presupuesto).filter(
        Presupuesto.id_usuario == usuario_actual.id,
        Presupuesto.id_categoria == datos.id_categoria,
        Presupuesto.mes == datos.mes,
        Presupuesto.anio == datos.anio
    ).first()

    if presupuesto_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un presupuesto para esta categoría en el mes indicado"
        )

    nuevo_presupuesto = Presupuesto(
        **datos.model_dump(),
        id_usuario=usuario_actual.id
    )

    sesion.add(nuevo_presupuesto)
    sesion.commit()
    sesion.refresh(nuevo_presupuesto)

    return nuevo_presupuesto


@enrutador.get(
    "/{id}",
    response_model=PresupuestoRespuesta,
    summary="Obtener presupuesto por ID"
)
def obtener_presupuesto(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve un presupuesto específico del usuario autenticado.
    """
    presupuesto = sesion.query(Presupuesto).filter(
        Presupuesto.id == id,
        Presupuesto.id_usuario == usuario_actual.id
    ).first()

    if not presupuesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presupuesto no encontrado"
        )

    return presupuesto


@enrutador.put(
    "/{id}",
    response_model=PresupuestoRespuesta,
    summary="Actualizar presupuesto existente"
)
def actualizar_presupuesto(
    id: int,
    datos: PresupuestoActualizar,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Actualiza los campos indicados de un presupuesto existente.
    Solo permite modificar presupuestos del usuario autenticado.
    """
    presupuesto = sesion.query(Presupuesto).filter(
        Presupuesto.id == id,
        Presupuesto.id_usuario == usuario_actual.id
    ).first()

    if not presupuesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presupuesto no encontrado"
        )

    # Actualiza solo los campos enviados en la petición
    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(presupuesto, campo, valor)

    sesion.commit()
    sesion.refresh(presupuesto)

    return presupuesto


@enrutador.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar presupuesto"
)
def eliminar_presupuesto(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Elimina un presupuesto del usuario autenticado.
    """
    presupuesto = sesion.query(Presupuesto).filter(
        Presupuesto.id == id,
        Presupuesto.id_usuario == usuario_actual.id
    ).first()

    if not presupuesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presupuesto no encontrado"
        )

    sesion.delete(presupuesto)
    sesion.commit()