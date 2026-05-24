# Endpoints de presupuestos: CRUD completo + gasto real calculado
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.esquemas.presupuesto import (
    PresupuestoActualizar,
    PresupuestoConGasto,
    PresupuestoCrear,
    PresupuestoRespuesta
)
from app.modelos.categoria import Categoria
from app.modelos.presupuesto import Presupuesto
from app.modelos.transaccion import Transaccion
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints de presupuestos
enrutador = APIRouter()


@enrutador.get(
    "/con-gastos/",
    response_model=List[PresupuestoConGasto],
    summary="Listar presupuestos con gasto real calculado"
)
def listar_presupuestos_con_gastos(
    mes: Optional[int] = Query(None, description="Filtrar por mes (1-12)"),
    anio: Optional[int] = Query(None, description="Filtrar por año"),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve los presupuestos del usuario con el gasto real de cada categoría
    calculado filtrando por el mes y año de cada presupuesto.
    Evita múltiples llamadas al dashboard desde el frontend.
    """
    consulta = sesion.query(Presupuesto).filter(
        Presupuesto.id_usuario == usuario_actual.id
    )

    if mes:
        consulta = consulta.filter(Presupuesto.mes == mes)
    if anio:
        consulta = consulta.filter(Presupuesto.anio == anio)

    presupuestos = consulta.order_by(
        Presupuesto.anio.desc(),
        Presupuesto.mes.desc()
    ).all()

    # Carga todas las categorías necesarias en una sola query para evitar N+1
    ids_categoria = [p.id_categoria for p in presupuestos]
    categorias = {
        c.id: c.nombre
        for c in sesion.query(Categoria).filter(Categoria.id.in_(ids_categoria)).all()
    }

    resultado = []
    for presupuesto in presupuestos:
        # Gasto real filtrado por categoría, mes y año del presupuesto
        gasto_actual = sesion.query(
            func.coalesce(func.sum(Transaccion.importe), 0.0)
        ).filter(
            Transaccion.id_usuario == usuario_actual.id,
            Transaccion.id_categoria == presupuesto.id_categoria,
            Transaccion.tipo == "gasto",
            func.extract("month", Transaccion.fecha) == presupuesto.mes,
            func.extract("year", Transaccion.fecha) == presupuesto.anio
        ).scalar() or 0.0

        porcentaje_usado = round(
            (gasto_actual / presupuesto.importe_limite * 100)
            if presupuesto.importe_limite > 0 else 0.0,
            2
        )

        resultado.append(PresupuestoConGasto(
            id=presupuesto.id,
            id_usuario=presupuesto.id_usuario,
            id_categoria=presupuesto.id_categoria,
            importe_limite=presupuesto.importe_limite,
            mes=presupuesto.mes,
            anio=presupuesto.anio,
            nombre_categoria=categorias.get(presupuesto.id_categoria, "Sin categoría"),
            gasto_actual=gasto_actual,
            porcentaje_usado=porcentaje_usado
        ))

    return resultado


@enrutador.post(
    "/copiar-al-mes-siguiente/",
    response_model=List[PresupuestoRespuesta],
    status_code=status.HTTP_201_CREATED,
    summary="Copiar presupuestos del mes indicado al mes siguiente"
)
def copiar_al_mes_siguiente(
    mes: int = Query(..., description="Mes origen (1-12)"),
    anio: int = Query(..., description="Año origen"),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Copia todos los presupuestos del mes/año indicado al mes siguiente.
    Omite los que ya existan en el destino para evitar duplicados.
    """
    # Calcular mes y año destino
    if mes == 12:
        mes_destino = 1
        anio_destino = anio + 1
    else:
        mes_destino = mes + 1
        anio_destino = anio

    # Presupuestos del mes origen
    presupuestos_origen = sesion.query(Presupuesto).filter(
        Presupuesto.id_usuario == usuario_actual.id,
        Presupuesto.mes == mes,
        Presupuesto.anio == anio
    ).all()

    if not presupuestos_origen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay presupuestos en el mes indicado"
        )

    # IDs de categorías que ya tienen presupuesto en el mes destino
    ids_existentes = {
        p.id_categoria
        for p in sesion.query(Presupuesto).filter(
            Presupuesto.id_usuario == usuario_actual.id,
            Presupuesto.mes == mes_destino,
            Presupuesto.anio == anio_destino
        ).all()
    }

    creados = []
    for origen in presupuestos_origen:
        if origen.id_categoria in ids_existentes:
            continue

        nuevo = Presupuesto(
            importe_limite=origen.importe_limite,
            mes=mes_destino,
            anio=anio_destino,
            id_categoria=origen.id_categoria,
            id_usuario=usuario_actual.id
        )
        sesion.add(nuevo)
        creados.append(nuevo)

    sesion.commit()
    for p in creados:
        sesion.refresh(p)

    return creados


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