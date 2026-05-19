# Endpoints de transacciones recurrentes
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.esquemas.recurrente import (
    RecurrenteActualizar,
    RecurrenteCrear,
    RecurrenteRespuesta
)
from app.modelos.recurrente import Recurrente
from app.modelos.transaccion import Transaccion
from app.modelos.usuario import Usuario

enrutador = APIRouter()


def calcular_proxima_ejecucion(frecuencia: str, fecha_inicio: datetime, dia_repeticion: int = None) -> datetime:
    """Calcula la próxima fecha de ejecución según la frecuencia."""
    ahora = datetime.utcnow()

    if frecuencia == "diario":
        proxima = fecha_inicio
        while proxima <= ahora:
            proxima += timedelta(days=1)
        return proxima

    elif frecuencia == "semanal":
        proxima = fecha_inicio
        while proxima <= ahora:
            proxima += timedelta(weeks=1)
        return proxima

    elif frecuencia == "mensual":
        proxima = fecha_inicio.replace(day=dia_repeticion or fecha_inicio.day)
        while proxima <= ahora:
            if proxima.month == 12:
                proxima = proxima.replace(year=proxima.year + 1, month=1)
            else:
                proxima = proxima.replace(month=proxima.month + 1)
        return proxima

    elif frecuencia == "anual":
        proxima = fecha_inicio
        while proxima <= ahora:
            proxima = proxima.replace(year=proxima.year + 1)
        return proxima

    return fecha_inicio


def ejecutar_recurrentes_pendientes(sesion: Session, id_usuario: int):
    """
    Ejecuta los recurrentes pendientes creando las transacciones correspondientes.
    Se llama al cargar los recurrentes del usuario.
    """
    ahora = datetime.utcnow()

    recurrentes = sesion.query(Recurrente).filter(
        Recurrente.id_usuario == id_usuario,
        Recurrente.activo == True,
        Recurrente.proxima_ejecucion <= ahora
    ).all()

    for recurrente in recurrentes:
        if recurrente.fecha_fin and ahora > recurrente.fecha_fin:
            recurrente.activo = False
            continue

        nueva_transaccion = Transaccion(
            tipo=recurrente.tipo,
            importe=recurrente.importe,
            fecha=recurrente.proxima_ejecucion,
            descripcion=f"[Recurrente] {recurrente.descripcion}",
            id_usuario=recurrente.id_usuario,
            id_categoria=recurrente.id_categoria,
            id_cuenta=recurrente.id_cuenta
        )
        sesion.add(nueva_transaccion)

        recurrente.proxima_ejecucion = calcular_proxima_ejecucion(
            recurrente.frecuencia,
            recurrente.proxima_ejecucion,
            recurrente.dia_repeticion
        )

    sesion.commit()


@enrutador.get(
    "/",
    response_model=List[RecurrenteRespuesta],
    summary="Listar recurrentes del usuario"
)
def listar_recurrentes(
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve todos los recurrentes del usuario.
    Ejecuta automáticamente los pendientes antes de devolver la lista.
    """
    ejecutar_recurrentes_pendientes(sesion, usuario_actual.id)

    return sesion.query(Recurrente).filter(
        Recurrente.id_usuario == usuario_actual.id
    ).order_by(Recurrente.proxima_ejecucion).all()


@enrutador.post(
    "/",
    response_model=RecurrenteRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo recurrente"
)
def crear_recurrente(
    datos: RecurrenteCrear,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Crea un nuevo recurrente y calcula su próxima ejecución."""
    proxima = calcular_proxima_ejecucion(
        datos.frecuencia,
        datos.fecha_inicio,
        datos.dia_repeticion
    )

    nuevo_recurrente = Recurrente(
        **datos.model_dump(),
        id_usuario=usuario_actual.id,
        proxima_ejecucion=proxima
    )

    sesion.add(nuevo_recurrente)
    sesion.commit()
    sesion.refresh(nuevo_recurrente)

    return nuevo_recurrente


@enrutador.get(
    "/{id}",
    response_model=RecurrenteRespuesta,
    summary="Obtener recurrente por ID"
)
def obtener_recurrente(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Devuelve un recurrente específico del usuario."""
    recurrente = sesion.query(Recurrente).filter(
        Recurrente.id == id,
        Recurrente.id_usuario == usuario_actual.id
    ).first()

    if not recurrente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurrente no encontrado"
        )

    return recurrente


@enrutador.put(
    "/{id}",
    response_model=RecurrenteRespuesta,
    summary="Actualizar recurrente"
)
def actualizar_recurrente(
    id: int,
    datos: RecurrenteActualizar,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza un recurrente existente."""
    recurrente = sesion.query(Recurrente).filter(
        Recurrente.id == id,
        Recurrente.id_usuario == usuario_actual.id
    ).first()

    if not recurrente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurrente no encontrado"
        )

    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(recurrente, campo, valor)

    sesion.commit()
    sesion.refresh(recurrente)

    return recurrente


@enrutador.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar recurrente"
)
def eliminar_recurrente(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Elimina un recurrente del usuario."""
    recurrente = sesion.query(Recurrente).filter(
        Recurrente.id == id,
        Recurrente.id_usuario == usuario_actual.id
    ).first()

    if not recurrente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurrente no encontrado"
        )

    sesion.delete(recurrente)
    sesion.commit()


@enrutador.post(
    "/{id}/pausar",
    response_model=RecurrenteRespuesta,
    summary="Pausar o reanudar recurrente"
)
def pausar_recurrente(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Pausa o reanuda un recurrente."""
    recurrente = sesion.query(Recurrente).filter(
        Recurrente.id == id,
        Recurrente.id_usuario == usuario_actual.id
    ).first()

    if not recurrente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurrente no encontrado"
        )

    recurrente.activo = not recurrente.activo
    sesion.commit()
    sesion.refresh(recurrente)

    return recurrente