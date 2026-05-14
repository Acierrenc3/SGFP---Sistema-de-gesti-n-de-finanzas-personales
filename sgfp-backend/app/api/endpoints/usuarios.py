# Endpoints de usuarios: perfil y configuración
# Basado en: https://fastapi.tiangolo.com/tutorial/sql-databases/

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.core.seguridad import obtener_hash_contraseña
from app.db.sesion import obtener_sesion
from app.esquemas.usuario import UsuarioActualizar, UsuarioRespuesta
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints de usuarios
enrutador = APIRouter()


@enrutador.get(
    "/perfil",
    response_model=UsuarioRespuesta,
    summary="Obtener perfil del usuario autenticado"
)
def obtener_perfil(
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Devuelve los datos del perfil del usuario autenticado.
    """
    return usuario_actual


@enrutador.put(
    "/perfil",
    response_model=UsuarioRespuesta,
    summary="Actualizar perfil del usuario autenticado"
)
def actualizar_perfil(
    datos: UsuarioActualizar,
    sesion: Session = Depends(obtener_sesion),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Actualiza los datos del perfil del usuario autenticado.
    Si se indica una nueva contraseña, se hashea antes de guardar.
    """
    datos_actualizados = datos.model_dump(exclude_unset=True)

    # Si se actualiza la contraseña, la hashea antes de guardar
    if "contrasena" in datos_actualizados:
        datos_actualizados["contrasena_hash"] = obtener_hash_contraseña(
            datos_actualizados.pop("contrasena")
        )

    for campo, valor in datos_actualizados.items():
        setattr(usuario_actual, campo, valor)

    sesion.commit()
    sesion.refresh(usuario_actual)

    return usuario_actual