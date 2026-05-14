# Endpoints de cuentas: CRUD completo
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.esquemas.cuenta import (
    CuentaActualizar,
    CuentaCrear,
    CuentaRespuesta
)
from app.modelos.cuenta import Cuenta
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints de cuentas
enrutador = APIRouter()


@enrutador.get(
    "/",
    response_model=List[CuentaRespuesta],
    summary="Listar cuentas del usuario"
)
def listar_cuentas(
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve todas las cuentas del usuario autenticado.
    """
    cuentas = sesion.query(Cuenta).filter(
        Cuenta.id_usuario == usuario_actual.id
    ).order_by(Cuenta.nombre).all()

    return cuentas


@enrutador.post(
    "/",
    response_model=CuentaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva cuenta"
)
def crear_cuenta(
    datos: CuentaCrear,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Crea una nueva cuenta vinculada al usuario autenticado.
    """
    nueva_cuenta = Cuenta(
        **datos.model_dump(),
        id_usuario=usuario_actual.id
    )

    sesion.add(nueva_cuenta)
    sesion.commit()
    sesion.refresh(nueva_cuenta)

    return nueva_cuenta


@enrutador.get(
    "/{id}",
    response_model=CuentaRespuesta,
    summary="Obtener cuenta por ID"
)
def obtener_cuenta(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve una cuenta específica del usuario autenticado.
    """
    cuenta = sesion.query(Cuenta).filter(
        Cuenta.id == id,
        Cuenta.id_usuario == usuario_actual.id
    ).first()

    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )

    return cuenta


@enrutador.put(
    "/{id}",
    response_model=CuentaRespuesta,
    summary="Actualizar cuenta existente"
)
def actualizar_cuenta(
    id: int,
    datos: CuentaActualizar,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Actualiza los campos indicados de una cuenta existente.
    Solo permite modificar cuentas del usuario autenticado.
    """
    cuenta = sesion.query(Cuenta).filter(
        Cuenta.id == id,
        Cuenta.id_usuario == usuario_actual.id
    ).first()

    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )

    # Actualiza solo los campos enviados en la petición
    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(cuenta, campo, valor)

    sesion.commit()
    sesion.refresh(cuenta)

    return cuenta


@enrutador.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar cuenta"
)
def eliminar_cuenta(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Elimina una cuenta del usuario autenticado.
    """
    cuenta = sesion.query(Cuenta).filter(
        Cuenta.id == id,
        Cuenta.id_usuario == usuario_actual.id
    ).first()

    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )

    sesion.delete(cuenta)
    sesion.commit()