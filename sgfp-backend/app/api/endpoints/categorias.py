# Endpoints de categorías: CRUD completo
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.esquemas.categoria import (
    CategoriaActualizar,
    CategoriaCrear,
    CategoriaRespuesta
)
from app.modelos.categoria import Categoria
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints de categorías
enrutador = APIRouter()


@enrutador.get(
    "/",
    response_model=List[CategoriaRespuesta],
    summary="Listar categorías del usuario"
)
def listar_categorias(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: 'ingreso' o 'gasto'"),
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve las categorías del usuario autenticado
    junto con las categorías predefinidas del sistema (id_usuario=None).
    Permite filtrar por tipo (ingreso/gasto).
    """
    consulta = sesion.query(Categoria).filter(
        (Categoria.id_usuario == usuario_actual.id) |
        (Categoria.id_usuario == None)
    )

    # Aplica filtro opcional por tipo
    if tipo:
        consulta = consulta.filter(Categoria.tipo == tipo)

    return consulta.order_by(Categoria.nombre).all()


@enrutador.post(
    "/",
    response_model=CategoriaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría personalizada"
)
def crear_categoria(
    datos: CategoriaCrear,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Crea una nueva categoría personalizada vinculada al usuario autenticado.
    """
    nueva_categoria = Categoria(
        nombre=datos.nombre,
        icono=datos.icono,
        color=datos.color,
        tipo=datos.tipo,
        id_usuario=usuario_actual.id
    )

    sesion.add(nueva_categoria)
    sesion.commit()
    sesion.refresh(nueva_categoria)

    return nueva_categoria


@enrutador.get(
    "/{id}",
    response_model=CategoriaRespuesta,
    summary="Obtener categoría por ID"
)
def obtener_categoria(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve una categoría específica.
    Solo permite acceder a categorías del usuario autenticado
    o categorías predefinidas del sistema.
    """
    categoria = sesion.query(Categoria).filter(
        Categoria.id == id,
        (Categoria.id_usuario == usuario_actual.id) |
        (Categoria.id_usuario == None)
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    return categoria


@enrutador.put(
    "/{id}",
    response_model=CategoriaRespuesta,
    summary="Actualizar categoría existente"
)
def actualizar_categoria(
    id: int,
    datos: CategoriaActualizar,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Actualiza los campos indicados de una categoría personalizada.
    Solo permite modificar categorías del usuario autenticado,
    no las categorías predefinidas del sistema.
    """
    categoria = sesion.query(Categoria).filter(
        Categoria.id == id,
        Categoria.id_usuario == usuario_actual.id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada o no tienes permiso para modificarla"
        )

    # Actualiza solo los campos enviados en la petición
    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(categoria, campo, valor)

    sesion.commit()
    sesion.refresh(categoria)

    return categoria


@enrutador.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar categoría personalizada"
)
def eliminar_categoria(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Elimina una categoría personalizada del usuario autenticado.
    No permite eliminar categorías predefinidas del sistema.
    """
    categoria = sesion.query(Categoria).filter(
        Categoria.id == id,
        Categoria.id_usuario == usuario_actual.id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada o no tienes permiso para eliminarla"
        )

    sesion.delete(categoria)
    sesion.commit()