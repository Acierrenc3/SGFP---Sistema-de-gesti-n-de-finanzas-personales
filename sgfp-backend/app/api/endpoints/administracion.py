# Endpoints del panel de administración
# Basado en: https://fastapi.tiangolo.com/tutorial/dependencies/

from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.endpoints.autenticacion import obtener_usuario_actual
from app.db.sesion import obtener_sesion
from app.modelos.transaccion import Transaccion
from app.modelos.usuario import Usuario

enrutador = APIRouter()


# Esquemas de respuesta
class UsuarioAdminRespuesta(BaseModel):
    id: int
    nombre: str
    email: str
    moneda: str
    activo: bool
    es_admin: bool
    total_transacciones: int
    fecha_registro: datetime

    class Config:
        from_attributes = True


class EstadisticasGlobales(BaseModel):
    total_usuarios: int
    usuarios_activos: int
    total_transacciones: int
    total_ingresos: float
    total_gastos: float


def verificar_admin(
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
) -> Usuario:
    """Verifica que el usuario actual es administrador."""
    if not usuario_actual.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de administrador."
        )
    return usuario_actual


@enrutador.get(
    "/estadisticas",
    response_model=EstadisticasGlobales,
    summary="Obtener estadísticas globales"
)
def obtener_estadisticas(
    sesion: Session = Depends(obtener_sesion),
    admin: Usuario = Depends(verificar_admin)
):
    """Devuelve estadísticas globales de la plataforma."""
    hace_un_mes = datetime.utcnow() - timedelta(days=30)

    total_usuarios = sesion.query(func.count(Usuario.id)).scalar()
    usuarios_activos = sesion.query(func.count(Usuario.id)).filter(
        Usuario.activo == True
    ).scalar()

    total_transacciones = sesion.query(func.count(Transaccion.id)).scalar()

    total_ingresos = sesion.query(
        func.coalesce(func.sum(Transaccion.importe), 0)
    ).filter(Transaccion.tipo == 'ingreso').scalar()

    total_gastos = sesion.query(
        func.coalesce(func.sum(Transaccion.importe), 0)
    ).filter(Transaccion.tipo == 'gasto').scalar()

    return EstadisticasGlobales(
        total_usuarios=total_usuarios,
        usuarios_activos=usuarios_activos,
        total_transacciones=total_transacciones,
        total_ingresos=float(total_ingresos),
        total_gastos=float(total_gastos)
    )


@enrutador.get(
    "/usuarios",
    response_model=List[UsuarioAdminRespuesta],
    summary="Listar todos los usuarios"
)
def listar_usuarios(
    sesion: Session = Depends(obtener_sesion),
    admin: Usuario = Depends(verificar_admin)
):
    """Devuelve la lista completa de usuarios con sus estadísticas."""
    usuarios = sesion.query(Usuario).order_by(Usuario.id).all()

    resultado = []
    for usuario in usuarios:
        total_transacciones = sesion.query(
            func.count(Transaccion.id)
        ).filter(Transaccion.id_usuario == usuario.id).scalar()

        resultado.append(UsuarioAdminRespuesta(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            moneda=usuario.moneda,
            activo=usuario.activo,
            es_admin=usuario.es_admin,
            total_transacciones=total_transacciones,
            fecha_registro=usuario.id and datetime.utcnow()
        ))

    return resultado


@enrutador.put(
    "/usuarios/{id}/toggle-activo",
    summary="Activar o desactivar usuario"
)
def toggle_activo_usuario(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    admin: Usuario = Depends(verificar_admin)
):
    """Activa o desactiva un usuario."""
    usuario = sesion.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if usuario.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta"
        )

    usuario.activo = not usuario.activo
    sesion.commit()

    return {
        "mensaje": f"Usuario {'activado' if usuario.activo else 'desactivado'} correctamente",
        "activo": usuario.activo
    }


@enrutador.delete(
    "/usuarios/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario"
)
def eliminar_usuario(
    id: int,
    sesion: Session = Depends(obtener_sesion),
    admin: Usuario = Depends(verificar_admin)
):
    """Elimina un usuario y todos sus datos."""
    usuario = sesion.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if usuario.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )

    sesion.delete(usuario)
    sesion.commit()